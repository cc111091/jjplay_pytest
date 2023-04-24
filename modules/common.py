import os, json, time, shutil, subprocess
from faker import Faker
#===============================================
rootPath = os.path.dirname(os.path.realpath(__file__)).replace('/modules', '')
configsFile = os.path.join(rootPath,'configs/configs.json')
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


def excuteCmd(cmd, outputFilePath=None, outputText=False): # Should not select both of outputFilePath and outputText at same time.
    outputString = None
    if outputFilePath:
        FileOperation.checkDir(os.path.dirname(outputFilePath))
        subprocess.run(cmd, stdout=open(outputFilePath, "w"))
    elif outputText:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
        outputString = result.stdout
    else:
        subprocess.run(cmd)
    
    return outputString

def updateConfig(configFile, newConfig):
    FileOperation.modifyJsonFile(configFile, newConfig)
    config = FileOperation.readJsonFile(configFile)

    return config

def getValidationCode(phone, start_yyyy, start_mm, start_dd, end_yyyy, end_mm, end_dd, user='river01',pwd='123qwe'):
    pass

configs = FileOperation.readJsonFile(configsFile)
dateStr = time.strftime('%Y%m%d%H%M%S')

class TestUser():
    def generate(self,pwdLen=11, useChars=False):
        self.faker = Faker(locale='zh_CN')
        
        self.user = {
            'fullname': self.faker.name(),
            'username':self.faker.simple_profile()['username'],
            'phone': self.faker.phone_number(),
            'pwd': self.faker.password(special_chars=useChars, length=pwdLen)
        }

        return self.user

testuser = TestUser().generate()
