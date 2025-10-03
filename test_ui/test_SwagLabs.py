from playwright.sync_api import Page, expect
import os
import dotenv
from time import sleep

dotenv.load_dotenv(override=True)


def test_full_correct(page: Page):
    page.goto(os.getenv('site'))
    
    login = page.locator('#user-name')
    login.fill(os.getenv('user_correct'))
    
    password =  page.locator('#password')
    password.fill(os.getenv('passwd'))
    
    page.locator('#login-button').click()
    
    filter = page.locator('//*[@class="product_sort_container"]')
    filter.select_option('Price (high to low)')
    
    page.get_by_text('Add to cart').nth(0).click()
    
    page.locator('#shopping_cart_container').click()
   
    page.locator('#checkout').click()
    
    page.locator('#first-name').fill('Pupkin')
    page.locator('#last-name').fill('Ivan')
    page.locator('#postal-code').fill('800-333-343-35')
    
    page.locator('#continue').click()
    
    page.locator('#finish').click()    


def test_currect_login(page: Page):
    page.goto(os.getenv('site'))
    login = page.locator('#user-name')
    login.fill(os.getenv('user_correct'))
    password =  page.locator('#password')
    password.fill(os.getenv('passwd'))
    page.locator('#login-button').click()
    
    expect(page).to_have_url('https://www.saucedemo.com/inventory.html')
    

def test_uncurrect_login(page: Page):
    page.goto(os.getenv('site'))
    login = page.locator('#user-name')
    login.fill(os.getenv('user_lock'))
    password =  page.locator('#password')
    password.fill(os.getenv('passwd'))
    page.locator('#login-button').click()
    
    expect(page).to_have_url('**/inventory.html', message="Переход не произошел")