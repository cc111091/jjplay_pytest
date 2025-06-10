import time, random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# ========================================
user = {
    'account': '14785566152',
    'password': 'qwerty123'
}
depositType = ['支付宝', '微信', '钱包支付', '网银支付']
minDeposit = 100
maxDeposit = 1000
minWithdrawal = 30
maxWithdrawal = 200
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

def jj_login(driver, pageURL):
    driver.get(f"http://qah5.jjplaygo.com/")
    pageElement((By.XPATH, '//button[.="登录"]')).click()
    pageElement((By.ID, '帐号')).send_keys(user['account'])
    pageElement((By.ID, '密码')).send_keys(user['password'])
    time.sleep(3)
    pageElement((By.XPATH, '//button[@class="base-button"]')).click()
    time.sleep(3)

    driver.get(f"http://qah5.jjplaygo.com/{pageURL}")

def jj_deposit(amount, type):
    pageElement((By.XPATH, '//span[.="充值 "]')).click()
    pageElement((By.XPATH, f'//button[.="{type}"]')).click()
    time.sleep(1)
    # if type == depositType[3]:
    #     if amount >= 10 and amount <= 500:
    #         pageElement((By.XPATH, f'//div[.="10-500"]')).click()
    #     else:
    #         pageElement((By.XPATH, f'//div[.="600-1500"]')).click()
    pageElement((By.XPATH, '//div[@class="deposit-amount-input"]/input')).send_keys(amount)
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

def jj_withdrawal(n):
    pageElement((By.XPATH, '//span[.="提现 "]')).click()
    time.sleep(1)
    for i in range(1, n+1):
        print(f'\r{i}/{n}', end='')
        pageElement((By.XPATH, '//div[@class="withdrawal-input"]/input')).clear()
        time.sleep(1)
        pageElement((By.XPATH, '//div[@class="withdrawal-input"]/input')).send_keys(minWithdrawal+i)
        time.sleep(1)
        pageElement((By.XPATH, '//button[.="确 定"]')).click()
        time.sleep(1)
        pageElement((By.XPATH, '//button[@class="base-button alert-button"]')).click()
        time.sleep(1)
    time.sleep(3)


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
        # --- Login and redirect_url ---
        jj_login(driver, 'wallet')
        # --- If need pass the captcha manually ---
        # time.sleep(100)
        

        # --- Customized Part ---
        # add deposit transactions
        deposit = False
        depositNum = 100
        if deposit:
            print('--- Start deposit! ---')
            for i in range(1, depositNum+1):
                print(f'\r{i}/{depositNum}', end='')
                depositChoice = random.choice(depositType)
                jj_deposit(minDeposit+i, depositChoice)
            print('\nDone\n')
        # jj_depositTarget(10000000)

        # add withdrawal transactions
        withdrawal = True
        withdrawalNum = 100
        if withdrawal:
            print('--- Start withdrawal! ---')
            time.sleep(50)
            jj_withdrawal(withdrawalNum)
            print('\nDone\n')

        
    except Exception as error:
        print('Got error!', error)

    finally:
        time.sleep(3)
        driver.quit()
        print('--- End ---')
        time.sleep(3)

