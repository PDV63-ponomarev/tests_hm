from pytest import mark, fixture
from playwright.sync_api import Page, expect
import re
from conftest import fixture
import os

@mark.correct
def test_filtress_AZ(page:Page, login):
  
    login()
 
    page.select_option('//*[@class="product_sort_container"]', 'Name (A to Z)')
    items = page.locator('.inventory_item_name').all_text_contents()
  
    assert items == sorted(items), 'A-Z filter not working correctly'

@mark.correct
def test_filtress_ZA(page:Page, login):
 
    login()
 
    page.select_option('//*[@class="product_sort_container"]', 'Name (Z to A)')
    items = page.locator('.inventory_item_name').all_text_contents()

    assert items == sorted(items, reverse=True), 'Z-A filter not working correctly'

@mark.correct
def test_filtress_price_low(page:Page, login):
 
    login()
   
    page.select_option('//*[@class="product_sort_container"]', 'Price (low to high)')
    prices = page.locator('.inventory_item_price').all_text_contents()
    price_clear = [float(re.sub(r'[^\d.]', '', price)) for price in prices]
  
    assert price_clear == sorted(price_clear), 'Price dont sorted low to high'

@mark.correct
def test_filtress_price_high(page:Page, login):
   
    login()
   
    page.select_option('//*[@class="product_sort_container"]', 'Price (high to low)')
    prices = page.locator('.inventory_item_price').all_text_contents()
    price_clear = [float(re.sub(r'[^\d.]', '', price)) for price in prices]
    
    assert price_clear == sorted(price_clear, reverse=True), 'Price dont sorted high to low'

@mark.correct
def test_all_images_unique_correct(page: Page, login):
 
    login()
  
    def get_all_product_image_names(page: Page):
        page.wait_for_selector('[class="inventory_item_img"]')
        image_containers = page.locator('//img[@class="inventory_item_img"]')
        image_names = []         
       
        for i in range(image_containers.count()):
            try:
                container = image_containers.nth(i)
                container.scroll_into_view_if_needed()
                img_locator = container.first
                if img_locator.is_visible():
                    src = img_locator.get_attribute('src')                                       
                    if src:
                        filename = os.path.basename(src.split('?')[0])
                        image_names.append(filename)
                        print(f'Карточка {i}: {filename}')
                    else:
                        print(f'Карточка {i}: src не найден')
                else:
                    print(f'Карточка {i}: изображение не видимо')                  
            except Exception as e:
                print(f'Ошибка в карточке {i}: {e}')
                continue    
        return image_names
   
    image_names = get_all_product_image_names(page)
    assert len(image_names) >= 2, f'Нужно минимум 2 изображения для сравнения, найдено: {len(image_names)}'
    unique_names = set(image_names)
    duplicate_names = set([x for x in image_names if image_names.count(x) > 1])
    
    print('СТАТИСТИКА:')
    print(f'Всего изображений: {len(image_names)}')
    print(f'Уникальных имен: {len(unique_names)}')
    print(f'Дубликатов: {len(image_names) - len(unique_names)}') 
   
    if duplicate_names:
        print(f'Найдены дубликаты: {duplicate_names}')  
    assert len(image_names) == len(unique_names), \
        f'Найдены дубликаты изображений! Всего: {len(image_names)}, уникальных: {len(unique_names)}'
   
    print('Все изображения уникальны!')

@mark.incorrect
def test_all_images_unique_incorrect(page: Page, login_problem):
  
    login_problem()
  
    def get_all_product_image_names(page: Page):       
        page.wait_for_selector('[class="inventory_item_img"]')      
        image_containers = page.locator('//img[@class="inventory_item_img"]')    
        image_names = []                
        
        for i in range(image_containers.count()):
            try:
                container = image_containers.nth(i)
                container.scroll_into_view_if_needed()
                img_locator = container.first
                if img_locator.is_visible():
                    src = img_locator.get_attribute('src')                   
                    if src:
                        filename = os.path.basename(src.split('?')[0])
                        image_names.append(filename)
                        print(f'Карточка {i}: {filename}')
                    else:
                        print(f'Карточка {i}: src не найден')
                else:
                    print(f'Карточка {i}: изображение не видимо')                   
            except Exception as e:
                print(f'Ошибка в карточке {i}: {e}')
                continue
        return image_names
   
    image_names = get_all_product_image_names(page)  
    assert len(image_names) >= 2, f'Нужно минимум изображения для сравнения, найдено: {len(image_names)}'
    unique_names = set(image_names)
    duplicate_names = set([x for x in image_names if image_names.count(x) > 1])   
   
    print('СТАТИСТИКА:')
    print(f'Всего изображений: {len(image_names)}')
    print(f'Уникальных имен: {len(unique_names)}')
    print(f'Дубликатов: {len(image_names) - len(unique_names)}')

    if duplicate_names:
        print(f'Найдены дубликаты: {duplicate_names}')
    assert len(image_names) == len(unique_names), \
        f'Найдены дубликаты изображений! Всего: {len(image_names)}, уникальных: {len(unique_names)}'
   
    print('Все изображения уникальны!')
