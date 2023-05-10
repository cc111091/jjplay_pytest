import os, json, time, shutil
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.keys import Keys #keyboardValue
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from .. import main
from . import common
#===============================================
osName = common.configs['osName']
browserName = common.configs['browserName']
#===============================================
class DriverOperations():
    def pc_webDriver():
        driverOptions = common.configs['pc_driverOptions'][browserName]
        if browserName in 'chrome':
            from selenium.webdriver.chrome.service import Service as ChromeService
            from webdriver_manager.chrome import ChromeDriverManager

            options = webdriver.ChromeOptions()

            if driverOptions['headless']:
                # true=hidden, false=display
                options.add_argument('--headless') 
            if driverOptions['hide_automated']:
                # hide "Chrome is being controlled by automated software"
                options.add_experimental_option('excludeSwitches', ['enable-automation']) 

            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()), 
                options=options
            )
        elif browserName in 'edge':
            from selenium.webdriver.edge.service import Service as EdgeService
            from webdriver_manager.microsoft import EdgeChromiumDriverManager

            driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install()), 
            )

        elif browserName in 'firefox':
            from selenium.webdriver.firefox.service import Service as FirefoxService
            from webdriver_manager.firefox import GeckoDriverManager

            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()), 
            )
        
        elif browserName in 'safari':
            from selenium.webdriver import Safari
            from selenium.webdriver.safari.options import Options as SafariOptions

            options = SafariOptions()
            options.add_argument('--headless') 

            driver = webdriver.Safari(options=options)

        return driver
    
    def mobile_webDriver(self):
        pass


class WebOperation:
    def xpathElement(driver, xpath):
        try:
            return WebDriverWait(driver, common.configs['waitSeconds']).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except:
            return WebOperation.findXpathElement(driver, xpath)

    def elementObj(driver, element): #element: (By.XPATH, xpath); (By.ID, id)
        try:
            return WebDriverWait(driver, common.configs['waitSeconds']).until(EC.presence_of_element_located(element))
        except:
            return WebOperation.findElement(driver, element)

    def findXpathElement(driver, xpath):
        try:
            return driver.find_element(By.XPATH, xpath)
        except:
            assert False, f'Element Not Found: xpath({xpath})'
    
    def findElement(driver, element): #element: (By.XPATH)
        try:
            return driver.find_element(element)
        except:
            assert False, f'Element Not Found: {element}'
    
    def xpathElements(driver, xpath):
        try:
            return driver.find_elements(By.XPATH, xpath)
        except:
            return None

    def scroll2elementByXpath(driver, xpath):
        # element = WebOperation.xpathElement(driver, xpath)
        element = driver.find_element(By.XPATH, xpath)
        element.location_once_scrolled_into_view

        
    def checkPageLoaded(driver, waitSeconds, checkXpath):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        from selenium.common.exceptions import TimeoutException
        
        try:
            element_present = EC.presence_of_element_located((By.XPATH, checkXpath))
            WebDriverWait(driver, waitSeconds).until(element_present)
            return True
        except TimeoutException:
            return False
    
    def getPeromanceLog(driver):
        logs = driver.execute_script("var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")

        return logs

class XpathElementOperation:
    def inputText(driver, xpath, text, desc=None):
        WebOperation.xpathElement(driver, xpath).send_keys(text)
        if not desc:
            desc = 'input'
        LogController.info(f'{desc}: "{text}"')
    
    def uploadFile(driver, xpath, filePath, desc=None):
        WebOperation.xpathElement(driver, xpath).send_keys(filePath)
        LogController.info(f'upload {desc}: {filePath}')
        time.sleep(3)
    
    def sendBackspace(driver, xpath, repeat=1):
        for i in range(repeat):
            WebOperation.xpathElement(driver, xpath).send_keys(Keys.BACK_SPACE)

    def clickObject(driver, xpath, desc=None, firstTime=True, useJS=False):
        try:
            element = WebOperation.xpathElement(driver, xpath)
            if useJS:
                driver.execute_script("arguments[0].click();", element) 
            else:
                element.click()
            LogController.info('{}'.format(desc))
            time.sleep(3)
        except Exception as exception:
            if firstTime:
                WebOperation.scroll2elementByXpath(driver, xpath)
                XpathElementOperation.clickObject(driver, xpath, desc, firstTime=False, useJS=useJS)
            elif not firstTime and not useJS:
                XpathElementOperation.clickObject(driver, xpath, desc, firstTime, True)
            else:
                assert False, exception

    def selectOption(driver, xpath, visibleText):
        select = Select(WebOperation.xpathElement(driver, xpath))
        select.select_by_visible_text(visibleText)

    def getText(driver, xpath):
        return WebOperation.xpathElement(driver, xpath).text

    def getAttribute(driver, xpath, attributeName):
        return WebOperation.xpathElement(driver, xpath).get_attribute(attributeName)

    def getList(driver, ul_xpath, matchText=None):
        list_element = WebOperation.xpathElement(driver, ul_xpath)
        items = list_element.find_elements_by_tag_name('li')
        if matchText:
            for item in range(len(items)):
                if items[item].text in matchText:
                    return os.path.join(ul_xpath, f'li[{item}]')
        else:
            return [item.text for item in items]
    
    def getChildValue(parentElement, tagName):
            childs = parentElement.find_elements(By.TAG_NAME,tagName)
            return [child.text for child in childs]

    def getTable(driver, table_xpath, splitSymbol=' '):
        time.sleep(3)
        table = WebOperation.xpathElement(driver, table_xpath)
        rows = table.find_elements(By.TAG_NAME, 'tr')
        headers = rows[0].text.split(splitSymbol)
        data = []
        for rowNum, row in enumerate(rows):
            if rowNum != 0:
                tds = row.find_elements(By.TAG_NAME, 'td')
                tmp = {headers[index]:td.text for index, td in enumerate(tds)}
                data.append(tmp)

        return data

class CheckCondition:
    def elementPresent(driver, xpath, waitSeconds=10):
        try:
            elementLocated = EC.presence_of_element_located((By.XPATH, xpath))
            WebDriverWait(driver, waitSeconds).until(elementLocated)
            return True
        except Exception:
            return False
    
    def elementVisible(driver, xpath, waitSeconds=10):
        try:
            elementLocated = EC.visibility_of_element_located((By.XPATH, xpath))
            WebDriverWait(driver, waitSeconds).until(elementLocated)
            return True
        except Exception:
            return False
    
    def elementClickable(driver, xpath, waitSeconds=10):
        try:
            elementLocated = EC.element_to_be_clickable((By.XPATH, xpath))
            WebDriverWait(driver, waitSeconds).until(elementLocated)
            return True
        except Exception:
            return False

    def elementValueMatch(driver, xpath, value, waitSeconds=10):
        try:
            elementValue = WebOperation.xpathElement(driver, xpath).get_attribute('value')
            if elementValue in value:
                return True
            else:
                False
        except Exception:
            return False
    
    def elementValueContain(driver, xpath, value, waitSeconds=10):
        try:
            elementValue = WebOperation.xpathElement(driver, xpath).get_attribute('value')
            if value in elementValue:
                return True
            else:
                False
        except Exception:
            return False
    
    def textPresent(driver, text, waitSeconds=10):
        if text in driver.page_source:
            return True
        else:
            return False

    def checkTableRow(tableData, findData, primaryFieldName=None, exact=False): # findData is dictionary, ex: {'field1':'123', 'field2':'456'}
        checks = {k:False for k, v in findData.items()}
        result = -1
        rowNum = None

        for index, row in enumerate(tableData):
            allPass = 0
            for fieldName, value in findData.items():
                if str(row[fieldName]) in str(value):
                    checks[fieldName] = True
                    allPass += 1
            if allPass == len(checks):
                rowNum = index+1
                result = 1
                break
            elif primaryFieldName:
                if checks[primaryFieldName]:
                    rowNum = index+1
                    result = 0
                    break
            elif allPass:
                rowNum = index+1
                result = 0

        return result, rowNum, checks


class MsgFormat:
    def testStep(msg):
        return print(f'{msg}')

    def dangerResult(msg, newTag=None):
        if newTag:
            newTag = str(newTag)
            return f'\033[0;30;41m{newTag.center(8)}\033[0m {msg}'
        else:
            return f'\033[0;30;41m{"Error".center(8)}\033[0m {msg}'

    def successResult(msg, newTag=None):
        if newTag:
            newTag = str(newTag)
            return f'\033[0;30;42m{newTag.center(8)}\033[0m {msg}'
        else:
            return f'\033[0;30;42m{"OK".center(8)}\033[0m {msg}'

    def warningResult(msg, newTag=None):
        if newTag:
            newTag = str(newTag)
            return f'\033[0;30;43m{newTag.center(8)}\033[0m {msg}'
        else:
            return f'\033[0;30;43m{"Notic".center(8)}\033[0m {msg}'


class LogController:
    
    def __init__(self):
        import logging
        from logging.config import fileConfig

        fileConfig(os.path.join(common.rootPath, 'configs/loggingConfig.ini'))

        self.logger = logging.getLogger()
        self.loggerOpen = common.configs['loggerOpen']
        if common.configs['loggerSave']:
            fileHandler = logging.FileHandler(os.path.join(common.rootPath, f'logs/{common.dateStr}.log'))
            fileHandler.setFormatter(self.logger.handlers[0].formatter)
            self.logger.addHandler(fileHandler)

    def info(self, msg):
        if self.loggerOpen:
            self.logger.info(msg)
    def debug(self, msg):
        if self.loggerOpen:
            self.logger.debug(msg)
    
    def error(self, msg):
        if self.loggerOpen:
            self.logger.error(msg)

    def warn(self, msg):
        if self.loggerOpen:
            self.logger.warn(msg)