from pytest import mark, fixture
from playwright.sync_api import Page, expect
import os
import dotenv
from time import sleep
from conftest import fixture

dotenv.load_dotenv(override=True)

# pytest --headed -s -m hm

@mark.full
def test_full_correct(page: Page, login):
    login()
    
    page.select_option('//*[@class="product_sort_container"]', 'Price (high to low)')
   
    page.get_by_text('Add to cart').nth(0).click()
    
    page.click('#shopping_cart_container')
   
    page.click('#checkout')
    
    page.fill('#first-name', 'Pupkin')
    page.fill('#last-name', 'Ivan')
    page.fill('#postal-code', '800-333-343-35')
    
    page.click('#continue')
    
    page.click('#finish')    

@mark.smoke
def test_login_correct(page: Page):
    page.goto(os.getenv('site'))

    page.fill('#user-name', os.getenv('user_correct'))
  
    page.fill('#password', os.getenv('passwd'))

    page.click('#login-button')
    
    expect(page).to_have_url('https://www.saucedemo.com/inventory.html')
    
@mark.smoke
def test_login_incorrect(page: Page):
    page.goto(os.getenv('site'))

    
    page.fill('#user-name', os.getenv('user_lock'))

    page.fill('#password', os.getenv('passwd'))

    page.click('#login-button')
    

    expect(page).to_have_url(os.getenv('site'))

    error_mess = page.locator('[data-test="error"]')
    expect(error_mess).to_be_visible()

