# jjplay_pytest
 
## Requirements
- Python `3.7.2`
- pip `19.0.2`
- pytest `7.2.2`
- pytest-bdd `6.1.1` (for `Gherkin` syntax) 
- pytest-html `3.2.0` (for generate .html report file)
- requests `2.28.2`
- selenium `4.8.3`
- appium server `1.22.3`
- appium python client  `2.9.0`

### More Details
#### #pip

- Install
    ```
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    ```
    ```
    python3 get-pip.py
    ```
    ```
    rm get-pip.py
    ```

#### #pytest and plugins (pytest-bdd, pytest-html)
> 💡 pyteset-bdd (almost same as Behave)
> - Github: https://github.com/pytest-dev/pytest-bdd

1. Install
    ```shell=bash
    pip3 install pytest pytest-bdd pytest-html
    ```
2. Validation (💡 Ignore the error during collection)
    ```
    >>> pytest -v --no-summary
    ...
    metadata: {..., 'Plugins': {..., 'bdd': '5.0.0', 'html': '3.1.1'}}
    ...
    ```

#### #Selenium
> https://pypi.org/project/selenium/

- Install
    ```
    pip3 install selenium
    ```

#### #Appium
1. Need install node.js to install Appium server
    > https://nodejs.org/en/download
2. Install Appium Server
    ```
    npm install -g appium
    ```
3. Getting the Appium Python client [🔗](https://pypi.org/project/Appium-Python-Client/)
    ```
    pip3 install Appium-Python-Client
    ```
4. Install dependencies
    > 💡 before installing dependencies, need update Xcode to the latest version.
    ```
    brew install libimobiledevice --HEAD
    brew install carthage
    ```
    
#### #Webdriver Manager
1. Install
    ```
    pip3 install webdriver-manager
    ```
    

#### #requests
- Install
    ```
    pip3 install requests
    ```


## Reference
- [Appium XCUITest on Real iOS Devices](https://medium.com/@yashwant-das/appium-xcuitest-on-real-ios-devices-bd1ebe0dea55)