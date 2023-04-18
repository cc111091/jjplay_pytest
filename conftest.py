import pytest, os, time
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import modules.funcs as funcs
# import module.basic as basic
# from module.basic import users, mode, config, dateStr, fileFolder, waitSeconds, send_plain_email
# import module.featureFunc as featureFunc
#===============================================
rootPath = os.path.dirname(os.path.realpath(__file__))
configsFile = os.path.join(rootPath,'configs/configs.json')
# if mode in 'remote':
#     # remote webdriver (lambdaTest)
#     from module.basic import username, accessKey
#     assert username and accessKey, 'Please check username and accessKey value'
#===============================================
@pytest.fixture
def context():
    # print('context')
    class Context(object):
        pass
    return Context()

@pytest.fixture(autouse=True, scope='session')
def setup(request):
    # --- before_all ---
    context.configs = funcs.FileOperation.readJsonFile(configsFile)
    context.waitSeconds = context.configs['waitSecond']
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
                                        result = ' '*8
                                    resultText += f'    [{result.center(5)}] step{i}, {stepName}\n'
                                else:
                                    # print(f'    [{result.center(8)}] step{i}, {stepName}')
                                    resultText += f'    [{result.center(8)}] step{i}, {stepName}\n'

                                i += 1

                if not context.failed:
                    # emailSubject = f'{sesConfig["subject"]} [{mode}] - All Passed'
                    emailContent = resultText
                else:
                    # emailSubject = f'{sesConfig["subject"]} [{mode}] - {context.count["Failed"]}/{context.count["Passed"]+context.count["Failed"]} Failed'
                    emailContent = resultText
            else:
                # emailSubject = f'{sesConfig["subject"]} [{mode}] - Error'
                emailContent = 'Something Bad Happened.'
            
            # send_plain_email(ses, sesConfig['from'], sesConfig['to'], emailContent, emailSubject)
            # send_plain_email(ses, sesConfig['from'], ['ivy@xencapital.com'], emailContent, emailSubject)

        finally:
            time.sleep(context.waitSeconds)

    request.addfinalizer(fin)

def pytest_bdd_before_scenario(request, feature, scenario):

    # local webdriver
    options = funcs.DriverOperations.web_chroneDriver(context.configs['driverOptions'])
    driver = webdriver.Chrome(
        service=Service(context.configs['driverExec']), 
        options=options
    )

    driver.implicitly_wait(context.waitSeconds)
    driver.maximize_window()

    context.driver = driver
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
    context.driver.quit()
    time.sleep(3)
