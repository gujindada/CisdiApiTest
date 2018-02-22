#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author='Jingle,LEOMASTER.CO.LTD'

import os
from utils import yamlhandler as yaml
import time
import smtplib
from email.mime.text import MIMEText


class Email(object):
    def __init__(self):
        self.rootpath = os.path.dirname(os.getcwd())
        self.yamlpath = self.rootpath + '\conf\email.yaml'

    def readEmailConfig(self):
        emailconfig = yaml.read_yaml(self.yamlpath)
        return emailconfig

    def sendEmail(self):
        emailconfig = self.readEmailConfig()
        print ('邮件配置：',emailconfig)
        sender = emailconfig['sender']
        receiver = emailconfig['receiver']
        subject = emailconfig['subject']
        username = emailconfig['username']
        password = emailconfig['password']
        smtpserver = emailconfig['smtpserver']
        # 记录邮件发送时间
        timeformat = '%Y-%m-%d %X'
        t = time.strftime(timeformat,time.localtime())
        text = '请及时查看CisdiApi的报告，谢谢'
        msg = MIMEText('您好,'+text, 'text', 'utf-8')

        msg['Subject'] = subject

        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.set_debuglevel(1)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()

if __name__ == '__main__':
    email = Email()
    email.sendEmail()
