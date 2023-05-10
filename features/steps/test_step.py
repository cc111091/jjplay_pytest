import pytest, pytest_bdd, time
from pytest_bdd import scenario, scenarios, given, when, then, parsers
from modules.common import configs
import modules.funcs as funcs
from src.pages.base import BasePage
from src.pages.cmsPage import CMSPage
#===============================================
# scenarios('') # pytest.ini: bdd_features_base_dir
# scenarios('test_fullScenario.feature')
# scenarios('test_example.feature')
scenarios('test_cms.feature')
webURL = configs['webURL']
#===============================================
@then('return failed')
def step_impl():
    assert False, 'assert "Failed"'

@then('return passed')
def step_impl():
    pass

@then(parsers.parse('return "{result}"'))
def step_impl(result):
    if result.lower() in 'passed':
        pass
    elif result.lower() in 'failed':
        assert False, 'assert "Failed"'

@given('go to jjplay home page')
def step_impl(browser):
    browser.get(webURL)
    time.sleep(10)

@given('go to jjplay login page')
def step_impl(browser):
    browser.get(f'{webURL}/login')
    time.sleep(10)

@given('go to jjplay register page')
def step_impl(browser):
    browser.get(f'{webURL}/register')
    time.sleep(10)

@given('go to jjplay fogot-password page')
def step_impl(browser):
    browser.get(f'{webURL}/fogot-password')
    time.sleep(10)

@given(parsers.parse('Navigate to "{websiteName}"\'s "{pageName}" page'))
def step_impl(browser, websiteName, pageName):
    if 'jj' in websiteName.lower():
        browser.get(BasePage.jj_urls[pageName.lower()])
    elif 'cms' in websiteName.lower():
        browser.get(BasePage.cms_urls[pageName.lower()])

@given(parsers.parse('Login as "{user}" / "{password}"'))
def step_impl(browser, user, password):
    CMSPage(browser).login(username=user, password=password)

@then(parsers.parse('Search and get "{phone}"\'s newest validation code today'))
def step_impl(browser, phone):
    CMSPage(browser).enter_phone_number(phone)
    CMSPage(browser).submit_searchInfo()
    time.sleep(3)
    codes = CMSPage(browser).get_codes(phone)
    print(codes[0]['验证码'])
