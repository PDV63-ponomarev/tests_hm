from pytest import mark, fixture
from playwright.sync_api import Page, expect
import re


@mark.filters
def test_filtress_AZ(page:Page, login):
    login()
    
    page.select_option('//*[@class="product_sort_container"]', 'Name (A to Z)')

    items = page.locator('.inventory_item_name').all_text_contents()
    
    assert items == sorted(items), "A-Z filter not working correctly"

@mark.filters
def test_filtress_ZA(page:Page, login):
    login()
    
    page.select_option('//*[@class="product_sort_container"]', 'Name (Z to A)')

    items = page.locator('.inventory_item_name').all_text_contents()
    
    assert items == sorted(items, reverse=True), "Z-A filter not working correctly"

@mark.filters
def test_filtress_price_low(page:Page, login):
    login()
    
    page.select_option('//*[@class="product_sort_container"]', 'Price (low to high)')

    prices = page.locator('.inventory_item_price').all_text_contents()
    
    price_clear = [float(re.sub(r'[^\d.]', '', price)) for price in prices]

    assert price_clear == sorted(price_clear), "Price dont sorted low to high"

@mark.filters
def test_filtress_price_high(page:Page, login):
    login()
    
    page.select_option('//*[@class="product_sort_container"]', 'Price (high to low)')

    prices = page.locator('.inventory_item_price').all_text_contents()
    
    price_clear = [float(re.sub(r'[^\d.]', '', price)) for price in prices]

    assert price_clear == sorted(price_clear, reverse=True), "Price dont sorted high to low)"

