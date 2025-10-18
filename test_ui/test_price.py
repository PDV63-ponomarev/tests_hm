from pytest import mark, fixture
from playwright.sync_api import Page, expect
import re
from conftest import fixture
import os
from time import sleep

@mark.price
def test_price_equal(page:Page, login):
    login()

    price_one = page.locator('.inventory_item_price').nth(0).text_content()
    
    page.locator('.inventory_item_name').nth(0).click()
       
    assert price_one == page.locator('.inventory_details_price').text_content(), 'Prices not equal'
    
    page.click('#add-to-cart')
    page.click('.shopping_cart_link')

    assert price_one == page.locator('.inventory_item_price').nth(0).text_content(), 'Prices in basket not equal'

    page.click('#checkout')

    page.fill('#first-name', 'Pupkin')
    page.fill('#last-name', 'Ivan')
    page.fill('#postal-code', '800-333-343-35')
    page.click('#continue')
    
    assert price_one == page.locator('.inventory_item_price').nth(0).text_content(), 'Prices in check not equal'
    
    page_summ = page.locator('.summary_subtotal_label').text_content()

    price_clear = float(re.sub(r'[^\d.]', '', page_summ))
    price_one_clear = float(re.sub(r'[^\d.]', '', price_one))
    
    assert price_one_clear == price_clear, 'Prices in total not equal'

  
@mark.price
def test_price_summ(page:Page, login):
    login()
    price_one = page.locator('.inventory_item_price').nth(0).text_content()
    price_two = page.locator('.inventory_item_price').nth(1).text_content()

    page.get_by_text('Add to cart').nth(0).click()
    page.get_by_text('Add to cart').nth(0).click()
     
    page.click('.shopping_cart_link')

    assert price_one == page.locator('.inventory_item_price').nth(0).text_content(), 'Prices 1 in basket not equal'
    assert price_two == page.locator('.inventory_item_price').nth(1).text_content(), 'Prices 2 in basket not equal'

    page.click('#checkout')

    page.fill('#first-name', 'Pupkin')
    page.fill('#last-name', 'Ivan')
    page.fill('#postal-code', '800-333-343-35')
    page.click('#continue')
    
    assert price_one == page.locator('.inventory_item_price').nth(0).text_content(), 'Prices 1 in check not equal'
    assert price_two == page.locator('.inventory_item_price').nth(1).text_content(), 'Prices 2 in check not equal'

    page_summ = page.locator('.summary_subtotal_label').text_content()
    price_clear = float(re.sub(r'[^\d.]', '', page_summ))

    price_one = float(re.sub(r'[^\d.]', '', price_one))
    price_two = float(re.sub(r'[^\d.]', '', price_two))
    price_summ = sum([price_one, price_two])
    
    assert price_summ == price_clear, 'Prices summ in total not equal'


