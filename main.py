import os, time, shlex, argparse
import modules.common as common
import modules.sendEmailWithAttachment as sendEmailWithAttachment
#===============================================
reportFolder = os.path.join(common.rootPath, 'html-report')
common.FileOperation.checkDir(reportFolder)
#===============================================
parser = argparse.ArgumentParser(description='run pytest', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--os', type=str, dest='osName', default='', help='os options: ["macos", "windows", "ios", "android"]')
parser.add_argument('--browser', type=str, dest='browserName', default='', help='browser options: ["chrome", "edge", "firefox", "safari"]')
args = parser.parse_args()

if args.osName:
    common.configs['osName'] = args.osName
if common.configs['osName'] in ['macos', 'windows']:
    if args.browserName:
        common.configs['browserName'] = args.browserName
    reportFileName = f'report-{common.dateStr}-{common.configs["osName"]}-{common.configs["browserName"]}'
if common.configs['osName'] in ['ios', 'android']:
    if args.browserName:
        common.configs['browserName'] = args.browserName
    reportFileName = f'report-{common.dateStr}-{common.configs["osName"]}-{common.configs["browserName"]}'

# cmdStr = f'python3 -m pytest --alluredir {allure_dir}'
cmdStr = f'python3 -m pytest --html={reportFolder}/{reportFileName}.html --self-contained-html'

try:
    cmd = shlex.split(cmdStr)
    common.excuteCmd(cmd, None, False)

    

finally:
    if common.configs['sendEmail']:
        config = common.FileOperation.readJsonFile(common.configsFile)
        sendEmailWithAttachment.send(config['emailSubject'], htmlPath=f'{reportFolder}/{reportFileName}.html')
    print('--- END ---\n')