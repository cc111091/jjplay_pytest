import time
from appium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# $ vim ~/.bash_profile
# export ANDROID_HOME=~/Library/Android/sdk
# export PATH=${PATH}:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
# export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-20.jdk/Contents/Home
# export PATH=${PATH}$JAVA_HOME/bin

# get ANDROID_ID: `$ adb -s <UDID> shell settings get secure android_id`
# get UDID: `$ adb devices`
# get deviceName: `$ adb -s <UDID> shell getprop ro.product.model`
# get platformVersion: `$ adb -s <UDID> shell getprop ro.build.version.release`
# download specific version chromedriver: `$ npm install appium --chromedriver_version="2.16"`
# ** capablities's `deviceName` and `UDID` just need one of both

# ** before run:
# 1. check device's developer mode is enable, also browser's too.
#    - device: enable the USB debugging option.
#    - if device is OPPO: enable the OEM Unlock option and the Disable Permision Monitoring option.
# 2-1. start Appium: `$ appium`
# 2-2. start appium with auto-download newest chromedriver: `$ appium --allow-insecure chromedriver_autodownload`

# ** capablities's `browserName: Chrome` is not worked under Android 13 version: 
#    - https://github.com/appium/appium/issues/17492
#    - instead `browserName: Chrome`
#        - add `appPackage: com.android.chrome`
#        - add `appActivity: com.google.android.apps.chrome.Main`

desired_caps = {
    'platformName': 'Android',
    'platformVersion': '13',
    # 'deviceName': 'CPH2067',
    'udid': 'emulator-5554',
    # "browserName": "Chrome",
    # 'chromedriverExecutable': '',
    'automationName':'UiAutomator2',
    'appPackage': 'com.android.chrome',
    'appActivity': 'com.google.android.apps.chrome.Main',
    "noReset": "true"
}

driver = webdriver.Remote(
    command_executor = 'http://localhost:4723/wd/hub',
    desired_capabilities = desired_caps
)
driver.get('http://qah5.jjplaygo.com/')
time.sleep(30)
driver.quit()