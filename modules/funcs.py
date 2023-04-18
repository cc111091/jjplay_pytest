import os, json
from selenium import webdriver
#===============================================
#===============================================
class FileOperation:
    def checkDir(path):
        if not os.path.exists(path):
            os.makedirs(path)
    
    def readJsonFile(filePath):
        with open(filePath) as readFile:
            content = json.load(readFile)

        return content
    
    def modifyJsonFile(filePath, newData):
        with open(filePath, 'w') as f:
            f.write(json.dumps(newData, indent=4))
    
    def downloadFile(url, saveFile):
        import urllib.request, shutil

        with urllib.request.urlopen(url) as response, open(saveFile, 'wb') as out_file:
            shutil.copyfileobj(response, out_file) 

class DriverOperations:
    def web_chroneDriver(driverOptions):
        options = webdriver.ChromeOptions()

        if driverOptions['headless']:
            # true=hidden, false=display
            options.add_argument('--headless') 
        if driverOptions['hide_automated']:
            # hide "Chrome is being controlled by automated software"
            options.add_experimental_option('excludeSwitches', ['enable-automation']) 

        return options