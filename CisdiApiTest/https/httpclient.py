#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author='Jingle,LEOMASTER.CO.LTD'

import requests
from utils import jsonhandler
import json
import re
import base64
import time


class HttpClient(object):

    '''
        request_info：单个接口信息的字典
    '''
    def __init__(self, request_info):
        self.url = request_info['url']
        self.headers = request_info['headers']
        self.params = request_info['params']
        self.body = request_info['body']
        self.method = request_info['method']

    # 初始判定返回数据格式，状态码

    @staticmethod
    def structure_judge(res):
        '''
            res: 上一个接口返回的json数据
        '''
        res_status = res.status_code
        print ('接口返回状态码：',res_status)
        if res_status == 200:
            res_content = res.content
            if jsonhandler.is_json(res_content):
                res_json = res_content
            else:
                default = {'code': 0, 'message': 'return data format is not JSON!'}
                res_json = json.dumps(default, ensure_ascii=False)
        else:
            default = {'code': 0, 'message': 'return status is not 200!'}
            res_json = json.dumps(default, ensure_ascii=False)
        return res_json

    # 获取前一个接口返回的参数内容，针对params、body和headers

    def get_precontent(self, reportDict):
        '''
            precontent: 上一个接口返回的json数据
        '''
        # 处理params
        if self.params is not None:
            for key in self.params:
                if type(self.params[key]) == str and '--' in self.params[key]:
                    keypath = self.params[key]

                    keylist = keypath.split('--')
                    httpkey = keylist[0]
                    print('引参参数名称：', keylist[-1])
                    print('引参接口名称：', httpkey)
                    precontent = reportDict[httpkey]['realReceptData']
                    print('引参数据源（指定接口返回数据）：', precontent)
                    key2 = keylist[1]
                    d = precontent[key2]

                    for i, key3 in enumerate(keylist):
                        if i >= 2:
                            if type(d)==list and re.compile('^[0-9]*$').match(key3)and len(d)>int(key3):
                                d = d[int(key3)]
                            elif type(d)==dict and d.has_key(key3):
                                d = d[key3]
                            else:
                                d = 'Out range index of List,Or the key is not exist'
                        i += 1
                    print('引参数据：', d)
                    self.params[key] = d

        # 处理body,支持json格式的body
        if self.body is not None and type(self.body) == dict:
            for key in self.body:
                if type(self.body[key])==str and '--' in self.body[key]:
                    keypath = self.body[key]

                    keylist = keypath.split('--')
                    httpkey = keylist[0]
                    print('引参参数名称：',keylist[-1])
                    print('引参接口名称：',httpkey)
                    precontent = reportDict[httpkey]['realReceptData']
                    print('引参数据源（指定接口返回数据）：', precontent)
                    key2 = keylist[1]
                    d = precontent[key2]

                    for i, key3 in enumerate(keylist):
                        if i >= 2:
                            if type(d)==list and re.compile('^[0-9]*$').match(key3)and len(d)>int(key3):
                                d = d[int(key3)]
                            elif type(d)==dict and d.has_key(key3):
                                d = d[key3]
                            else:
                                d = 'Out range index of List,Or the key is not exist'
                        i += 1
                    print('引参数据：', d)
                    self.body[key] = d
        # body 预处理机制
        elif self.body is not None and type(self.body) == list:
            self.body = json.dumps(self.body)
            print("如果body是list：")
            print(self.body)
        # 处理headers
        if self.headers is not None:
            for key in self.headers:
                if type(self.headers[key])==str and '--' in self.headers[key]:
                    keypath = self.headers[key]

                    keylist = keypath.split('--')
                    httpkey = keylist[0]
                    print ('引参参数名称：',keylist[-1])
                    print ('引参接口名称：',httpkey)
                    precontent = reportDict[httpkey]['realReceptData']
                    print ('引参数据源（指定接口返回数据）：',precontent)
                    key2 = keylist[1]
                    d = precontent[key2]

                    for i, key3 in enumerate(keylist):
                        if i >= 2:
                            if type(d)==list and re.compile('^[0-9]*$').match(key3)and len(d)>int(key3):
                                d = d[int(key3)]
                            elif type(d)==dict and d.has_key(key3):
                                d = d[key3]
                            else:
                                d = 'Out range index of List,Or the key is not exist'
                        i += 1
                    print ('引参数据：',d)
                    self.headers[key] = d
                    # 没得法，只能在这里对token的继承特殊处理。。。。
                if key.lower() == 'authorization':
                    authorization = 'Bearer '+self.headers[key]
                    domainId = self.headers['domainId']
                    # 先转成二进制
                    domainId = domainId.encode(encoding="utf-8")
                    # print(type(domainId))
                    tail = base64.b64encode(domainId)
                    # base64编码后转成str
                    tail = tail.decode()
                    self.headers[key] = authorization + '.' + tail
                    print('最终的authorization：\n'+str(self.headers[key]))

    def http_request(self, reportDict={}):

        if self.method.lower() == 'get':
            # 先对params和body做继承处理
            self.get_precontent(reportDict)
            time_start = time.time()
            res = requests.get(url=self.url, params=self.params, headers=self.headers, verify=False)
            time_end = time.time()
            # 统计单个接口访问时间
            time_dura = str(round(float(time_end-time_start), 2))
            # 接口返回的数据格式必须是json，且状态码为200
            res_json = self.structure_judge(res)
        elif self.method.lower() == 'post':
            self.get_precontent(reportDict)
            time_start = time.time()
            res = requests.post(url=self.url, data=self.body,
                                headers=self.headers, verify=False)
            time_end = time.time()
            time_dura = str(round(float(time_end-time_start), 2))
            res_json = self.structure_judge(res)
        else:
            res_json = json.dumps({'message':'the method of request is Invalid!'}, ensure_ascii=False)
            time_dura = str(0.00)

        return res_json, time_dura


if __name__ == '__main__':

    tail = base64.b64encode("dc7c381415064292aea5c19cc7935582")
    print (tail)
    '''
    request_info = {
        'method': 'get',
        'url': 'http://httpbin.org/get',
        'params': {'hello': 'hello'},
        'body': None,
        'headers': None
    }
    request_info2 = {
        'method': 'post',
        'url': 'http://httpbin.org/post',
        'params': None,
        'body': {'hello': 'args--hello'},
        'headers': None
    }
    httpClient = HttpClient(request_info)
    res_json = httpClient.http_request()
    print res_json
    httpClient2 = HttpClient(request_info2)
    res_json2 = httpClient2.http_request(json.loads(res_json))
    print res_json2
    print httpClient2.body'''


