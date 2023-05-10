import os, time
from conftest import context
import modules.funcs as funcs
from seleniumpagefactory.Pagefactory import PageFactory
    

class CMSPage(PageFactory):

    locators = {
        'username_input': ('ID', 'Username'), #'//*[@id="Username"]'
        'pwd_input': ('ID', 'Password'), #'//*[@id="Password"]'
        'submit_btn': ('XPATH', '//button[@type=\'submit\']'),
        'code_table': ('XPATH', '//table[@class=\'first-child\']'),
        'phone_input': ('ID', 'Mobile'),
        'search_btn': ('ID', 'search')
    }
    

    def __init__(self, driver):
        self.driver = driver

    def login(self, username='river01', password='123qwe'):
        self.username_input.set_text(username)
        self.pwd_input.set_text(password)
        self.submit_btn.click_button()

        time.sleep(3)

    def enter_phone_number(self, phone):
        self.phone_input.set_text(phone)

    def submit_searchInfo(self):
        self.search_btn.click_button()
    
    def get_codes(self, phone):
        codes = funcs.XpathElementOperation.getTable(self.driver, self.locators['code_table'][1])

        assert codes, f'Not Found: not found the validation code of phone \'{phone}\' today.'
        # return codes[0]['验证码']
        return codes