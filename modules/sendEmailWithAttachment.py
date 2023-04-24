from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
import smtplib
from string import Template

def send(subject, text="", htmlPath=None, attachment=None):
    content = MIMEMultipart()
    content['subject'] = subject
    content['from'] = 'ivy@auro.gg'
    content['to'] = 'ivy@auro.gg'
    if htmlPath:
        template = open(htmlPath)
        content.attach(MIMEText(template.read(), 'html'))
    else:
        content.attach(MIMEText(text))

    with smtplib.SMTP(host='smtp.gmail.com', port='587') as smtp:
        try:
            smtp.ehlo()
            smtp.starttls()
            smtp.login('ivy@auro.gg', 'byblwxxwdhvvmrjd')
            smtp.send_message(content)
        except Exception as e:
            print(f'Error message: {e}')

# send('macos [chrome] - 2/4 Failed', htmlPath='/Users/admin/Downloads/workspace/jjplay_pytest/html-report/report-20230418174642-macos-chrome.html')