import pytest, os, time
import modules.common as common
import modules.funcs as funcs
import modules.sendEmailWithAttachment as sendEmailWithAttachment
from faker import Faker
#===============================================
#===============================================
@pytest.fixture
def context():
    # print('context')
    class Context(object):
        pass
    return Context()

@pytest.fixture
def browser():
    if context.configs['osName'] in ['macos', 'windows']:
        driver = funcs.DriverOperations.pc_webDriver()
        driver.implicitly_wait(context.waitSeconds)
        driver.maximize_window()
    else:
        driver = funcs.DriverOperations.mobile_webDriver()

    yield driver

    time.sleep(3)
    driver.quit()
    time.sleep(3)

@pytest.fixture
def urls():
    class URLs():
        jj_baseURL = 'http://qah5.jjplaygo.com'
        jj_home = jj_baseURL
        jj_register = f'{jj_baseURL}/register'
        jj_login = f'{jj_baseURL}/login'
        jj_forgotPassword = f'{jj_baseURL}/forgot-password'
        jj_wallet = f'{jj_baseURL}/wallet'
        jj_withdraw = f'{jj_baseURL}/withdraw'
        jj_deposit = f'{jj_baseURL}/deposit'
        jj_history = f'{jj_baseURL}/history'
        jj_profile = f'{jj_baseURL}/profile'
        jj_nickname = f'{jj_baseURL}/nickname'
        jj_fullname = f'{jj_baseURL}/fullname'
        jj_phone = f'{jj_baseURL}/phone'
        jj_password = f'{jj_baseURL}/password'
        jj_language = f'{jj_baseURL}/language'
        jj_tasks = f'{jj_baseURL}/tasks'
        jj_promo = f'{jj_baseURL}/promo'
        jj_notifications = f'{jj_baseURL}/notifications'
        jj_games = f'{jj_baseURL}/games'
        jj_referral = f'{jj_baseURL}/referral'
        jj_share = f'{jj_baseURL}/share'
        jj_agent = f'{jj_baseURL}/agent'
        jj_about = f'{jj_baseURL}/about'
        jj_help = f'{jj_baseURL}/help'

        cms_baseURL = 'http://20.24.16.242:8002'
        cms_home = cms_baseURL
        cms_customers = f'{cms_baseURL}/customers/search'
        cms_mobileverificationcode = f'{cms_baseURL}/mobileverificationcode/search'
        cms_urls = {
            'home': cms_home,
            'customers': cms_customers,
            'mobileverificationcode': cms_mobileverificationcode
        }

        
    return URLs


@pytest.fixture(autouse=True, scope='session')
def setup(request):
    # --- before_all ---
    context.configs = common.configs
    context.waitSeconds = context.configs['waitSeconds']
    context.varDic = {}
    context.results = {}
    context.failed = False
    context.count = {"Passed":0,"Failed":0}

    def fin():
        # --- after_all ---
        try:
            resultText = ''
            # sesConfig = config['aws_ses']
            # ses = boto3.client('ses', region_name='us-east-1')
            if context.results:
                for featureName, scenarios in context.results.items():
                    # print(f'\nFeature: {featureName}')
                    resultText += f'Feature: {featureName}\n'
                    scenarioNames = [name for s in scenarios for name, steps in s.items()]
                    count = {}
                    exampleNum = 1
                    for scenario in scenarios:
                        for scenarioName, steps in scenario.items():
                            try:
                                tmp = count[scenarioName]
                            except:
                                count[scenarioName] = scenarioNames.count(scenarioName)
                            if count[scenarioName] > 1:
                                # print(f'  scenario: {scenarioName} -- #{exampleNum}/{count[scenarioName]}')
                                resultText += f'  scenario: {scenarioName} -- #{exampleNum}/{count[scenarioName]}\n'
                                if count[scenarioName] > exampleNum:
                                    exampleNum += 1
                                elif count[scenarioName] == exampleNum:
                                    exampleNum = 1
                            else:
                                # print(f'  scenario: {scenarioName}')
                                resultText += f'  scenario: {scenarioName}\n'
                            i = 1
                            for stepName, result in steps.items():
                                if result in '' and not context.configs['emojiResult']:
                                    result = ' '*13
                                elif 'failed' in result.lower() and not context.failed:
                                    context.failed = True
                                
                                if context.configs['emojiResult']:
                                    if 'passed' in result.lower():
                                        result = '✅'
                                    elif 'failed' in result.lower():
                                        result = '❌'
                                    else:
                                        result = ' '*5
                                    resultText += f'    [{result.center(5)}] step{i}, {stepName}\n'
                                else:
                                    # print(f'    [{result.center(8)}] step{i}, {stepName}')
                                    resultText += f'    [{result.center(8)}] step{i}, {stepName}\n'

                                i += 1

                if not context.failed:
                    emailSubject = f'{context.configs["osName"]} [{context.configs["browserName"]}] - All Passed✅'
                else:
                    emailSubject = f'{context.configs["osName"]} [{context.configs["browserName"]}] - {context.count["Failed"]}/{context.count["Passed"]+context.count["Failed"]} Failed❌'
                emailContent = resultText
            else:
                # emailSubject = f'{sesConfig["subject"]} [{mode}] - Error'
                emailContent = 'Something Bad Happened.'
            
            # send_plain_email(ses, sesConfig['from'], sesConfig['to'], emailContent, emailSubject)
            # send_plain_email(ses, sesConfig['from'], ['ivy@xencapital.com'], emailContent, emailSubject)
            if context.configs['sendEmail']:
                common.configs['emailSubject'] = emailSubject
                common.FileOperation.modifyJsonFile(common.configsFile, common.configs)
            

        finally:
            time.sleep(context.waitSeconds)
        

    request.addfinalizer(fin)


def pytest_bdd_before_scenario(request, feature, scenario):
    context.scenarioFailed = False
    context.varDic['tmpScenario'] = {scenario.name:{step.name:'' for step in scenario.steps}}

def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    context.varDic['tmpScenario'][scenario.name][step.name] = 'Passed'

def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    context.varDic['tmpScenario'][scenario.name][step.name] = 'Failed'
    context.failed = True
    context.scenarioFailed = True

def pytest_bdd_after_scenario(request, feature, scenario):
    try:
        context.results[feature.name].append(context.varDic['tmpScenario'])
    except KeyError:
        context.results[feature.name] = [context.varDic['tmpScenario']]
    
    if context.scenarioFailed:
        context.count['Failed'] += 1
    else:
        context.count['Passed'] += 1
    
    time.sleep(3)
    
