import pytest, pytest_bdd, time
from conftest import context
from pytest_bdd import scenario, scenarios, given, when, then, parsers
from modules.common import configs
import modules.funcs as funcs
#===============================================
# scenarios('') # pytest.ini: bdd_features_base_dir
# scenarios('test_fullScenario.feature')
# scenarios('test_example.feature')
scenarios('test_forgotPassword.feature')
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
def step_impl():
    context.driver.get(webURL)
    time.sleep(10)

@given('go to jjplay login page')
def step_impl():
    context.driver.get(f'{webURL}/login')
    time.sleep(10)

@given('go to jjplay register page')
def step_impl():
    context.driver.get(f'{webURL}/register')
    time.sleep(10)

@given('go to jjplay fogot-password page')
def step_impl():
    context.driver.get(f'{webURL}/fogot-password')
    time.sleep(10)


def get_code(phone):
    user, pwd = 'river01', '123qwe'
    yyyy, mm, dd = time.strftime('%Y'), time.strftime('%m'), time.strftime('%d')
    context.driver.execute_script('window.open('');')
    # Switch to the new window
    context.driver.switch_to.window(context.driver.window_handles[1])
    context.driver.get(f'http://20.24.16.242:8002/mobileverificationcode/search?PageNumber=1&PageSize=10&OrderBy=Id&IsAscending=false&Mobile={phone}&CreateDateRange={yyyy}%2F{mm}%2F{dd}+00%3A00%3A00-{yyyy}%2F{mm}%2F{dd}+23%3A59%3A59&VerifiedDateRange=')
    
    time.sleep(3)

    input_username = '//*[@id="Username"]'
    input_pwd = '//*[@id="Password"]'
    btn_submit = '//button[@type=\'submit\']'

    funcs.XpathElementOperation.inputText(context.driver, input_username, user, 'Username')
    funcs.XpathElementOperation.inputText(context.driver, input_pwd, pwd, 'Password')
    funcs.XpathElementOperation.clickObject(context.driver, btn_submit, 'Submit')

    table_code = '//table[@class=\'first-child\']'

    data_code = funcs.XpathElementOperation.getTable(context.driver, table_code)
    return data_code[0]['验证码']
    
