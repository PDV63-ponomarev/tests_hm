from playwright.sync_api import Page
from pytest import fixture
import os

@fixture
def login(page: Page):
    def _login():
        page.goto(os.getenv('site'))
        page.fill('#user-name', os.getenv('user_correct'))
        page.fill('#password', os.getenv('passwd'))
        page.click('#login-button')
    return _login

@fixture
def login_problem(page: Page):
    def _login():
        page.goto(os.getenv('site'))
        page.fill('#user-name', os.getenv('user_problem'))
        page.fill('#password', os.getenv('passwd'))
        page.click('#login-button')
    return _login
