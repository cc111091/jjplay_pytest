import time, random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# ========================================
user = {
    'account': 'testuser10',
    'password': 'qwertyuiop'
}
depositType = ['支付宝', '微信', '钱包支付', '网银支付']
minDeposit = 10
maxDeposit = 1000
# ========================================
def browser():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), 
        options=options
    )

    yield driver

    time.sleep(3)
    driver.quit()
    time.sleep(3)

def findXpathElement(driver, xpath):
    try:
        return driver.find_element(By.XPATH, xpath)
    except:
        assert False, f'Element Not Found: xpath({xpath})'

def xpathElement(driver, xpath):
    try:
        return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except:
        return findXpathElement(driver, xpath)

def pageElement(selector):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located(selector))

def jj_login(driver, redirectURL):
    driver.get(f"http://qah5.jjplaygo.com/login?redirect={redirectURL}")
    pageElement((By.ID, '帐号')).send_keys(user['account'])
    pageElement((By.ID, '密码')).send_keys(user['password'])
    pageElement((By.XPATH, '//button[.="登 录"]')).click()
    time.sleep(3)

def jj_deposit(amount, type):
    pageElement((By.XPATH, '//div[@class="row-bottom"]/button[2]')).click()
    pageElement((By.XPATH, f'//button[.="{type}"]')).click()
    if type == depositType[3]:
        if amount >= 10 and amount <= 500:
            pageElement((By.XPATH, f'//div[.="10-500"]')).click()
        else:
            pageElement((By.XPATH, f'//div[.="600-1500"]')).click()
    pageElement((By.XPATH, '//input')).send_keys(amount)
    time.sleep(1)
    pageElement((By.XPATH, '//button[.="确 定"]')).click()
    time.sleep(1)
    pageElement((By.XPATH, '//button[.="完 成"]')).click()
    time.sleep(3)

def jj_randomDepositTransaction(amount, randomAmount=False):
    depositChoice = random.choice(depositType)
    amount = random.randint(minDeposit, maxDeposit) if randomAmount else amount
    jj_deposit(amount, depositChoice)

def jj_depositTarget(target, randomType=True, depositType=None):
    amounts = [maxDeposit]*(target//maxDeposit)
    amounts.append(target%maxDeposit)
    if randomType:
        for amount in amounts:
            jj_randomDepositTransaction(amount)
    else:
        for amount in amounts:
            jj_deposit(amount, depositType)
    


# ----------------------------------------
if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), 
        options=options
    )

    driver.set_window_position(0, 0)
    driver.set_window_size(2560, 1440)

    try:
        # Login and redirect_url
        # jj_login(driver, '/wallet')
        # need pass the captcha manually
        time.sleep(100)
        

        # Customized Part
        
        # for amount in range(140, 201):
        #     depositChoice = random.choice(depositType)
        #     jj_deposit(amount, depositChoice)

        # jj_depositTarget(10000000)
    except:
        print('got error!')

    finally:
        time.sleep(3)
        driver.quit()
        time.sleep(3)

