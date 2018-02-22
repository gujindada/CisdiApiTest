#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author='Jingle,LEOMASTER.CO.LTD'

import os
from utils import yamlhandler as yaml
from utils import loghandler as log
import requests
import json
import time


class Send(object):
    def __init__(self):
        self.rootpath = os.path.dirname(os.getcwd())
        self.yamlpath = self.rootpath + '\conf\send.yaml'
        self.sendconfig = yaml.read_yaml(self.yamlpath)
        timeformat = '%Y-%m-%d %X'
        t = time.strftime(timeformat,time.localtime())
        self.currentTime = t
        # 初始化获取access_token
        params = {'grant_type': 'client_credential',
                  'appid': self.sendconfig['appid'],
                  'secret': self.sendconfig['secret']}
        res = requests.get(url='https://open.qingtui.im/v1/token', params=params, verify=False)
        content = json.loads(res.content)
        print('获取发送token及其它内容：',content)
        self.access_token = content['access_token']

    def sendMultiUser(self):
        touser = self.sendconfig['touser']
        print ('接收人清单OpenId：',touser)
        data = {'touser': touser,
                'text':{'content': 'The Api Test has finished, please receive the nearest report of '+self.currentTime},
                'msgtype': 'text'}
        params = {'access_token': self.access_token}
        data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        #print data
        res = requests.post(url='https://open.qingtui.im/v1/message/mass/send',
                            params=params,
                            data=data,
                            headers=headers,
                            verify=False)
        if res.status_code == 200:
            print ('测试完成通知已发送')
            log.logINFO('测试完成通知已发送')
        else:
            print ('测试完成通知，发送失败')
            log.logINFO('测试完成通知，发送失败')

if __name__ == '__main__':
    send = Send()
    send.sendMultiUser()




