import os, time
import modules.funcs as funcs
from pages.base import BasePage
from seleniumpagefactory.Pagefactory import PageFactory


class LoginPage(PageFactory):
    locators = {
        'account_input': ('ID', '帐号'),
        'password_input': ('ID', '密码'),
        'login_btn': ('XPATH', '//button[.="密码登录"]')
    }

    def __init__(self, driver):
        self.driver = driver

    def enter_account(self, account):
        self.account_input.set_text(account)

    def enter_password(self, password):
        self.password_input.set_text(password)

    def submit_loginInfo(self):
        self.login_btn.click_button()

    