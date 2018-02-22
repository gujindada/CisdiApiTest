#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author='Jingle,LEOMASTER.CO.LTD'

import os
import sys

# 初始化修改
d = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
print(d)
sys.path.append(d)

from handler import prehttp as pre
from utils import excel as excel
from https import httpclient as http
from Assert import Assert
from utils import loghandler as log
from utils import send as send
import json


def run_single(l, commonName):
    #step1单个案例配置信息传入
        # 报告存放路径
    reportPath = l['reportAddress']
    caseconfig, domain = pre.gen_caseconfig(l)
        # 案例集合，断言集合
    caseinfolist, assertinfolist, casenameList = pre.gen_caseinfo(caseconfig, domain)
    print ('接口执行顺序：',casenameList)
    log.logINFO('接口执行顺序：'+str(casenameList))
        # 初始化报告集合
    reportDict = {}
        # 开始跑遍历，
        # 关键信息是caseinfolist,assertinfolist,casenameList, 使用者可以根据自己喜好改写生成这三个参数的方法
    for i,val in enumerate(caseinfolist):
        print ('开始测试接口：'+casenameList[i]+'----------------------------------------------')
        log.logINFO('开始测试接口：'+str(casenameList[i])+'----------------------------------------------')
        request_info = caseinfolist[i]
        print (casenameList[i]+'  原始发送配置数据：'+str(request_info))
        log.logINFO(str(casenameList[i])+'  原始发送配置数据：'+str(request_info))
        checkKeyList = assertinfolist[i]['assertKey']
        expectValueList = assertinfolist[i]['assertContent']
        checkKey = ''
        expectValue = ''
        if checkKeyList == None:
            checkKey += "not check;"
            expectValue += "not check;"
        else:
            for i2 in range(len(checkKeyList)):
                checkKey += str(checkKeyList[i2]) + '; '
                expectValue += str(expectValueList[i2]['value']) + '; '
                i2 += 1

        reportDict[casenameList[i]] = {'ApiName': casenameList[i], 'url': request_info['url'],
                        'requestData': caseinfolist[i], 'realReceptData': '',
                        'checkKey': checkKey, 'checkResult': '',
                        'expectValue': expectValue, 'realValue': '',
                        'time': '', 'repeatTimes': ''}

        # 发送http/https请求
        httpClient = http.HttpClient(request_info)
        res_json, time_dura = httpClient.http_request(reportDict)
        print ('接收数据：',res_json)
        log.logINFO('接收数据：'+str(res_json))
        # 断言
        ass = Assert.Assert()
        assertResultList, realValueList = ass.get_assertResult(assertinfolist[i], json.loads(res_json))
        print ('断言结果：',assertResultList)
        log.logINFO('断言结果：'+str(assertResultList))
        assertResult = ''
        realValue = ''
        for i3 in range(len(assertResultList)):
            assertResult += str(assertResultList[i3]) + '; '
            realValue += str(realValueList[i3]) + '; '
            i3 += 1

        reportDict[casenameList[i]]['checkResult'] = assertResult
        reportDict[casenameList[i]]['realReceptData'] = json.loads(res_json)
        reportDict[casenameList[i]]['realValue']= realValue
        reportDict[casenameList[i]]['time']= time_dura
        print ('完成单个接口后的报告字典：', reportDict)
        log.logINFO('完成单个接口后的报告字典：'+str(reportDict))

    print('本轮测试完成--------------  ^*^ ^*^')
    log.logINFO('本轮测试完成--------------  ^*^ ^*^')
        # 建立报告
    reportName = excel.create_report(reportDict, casenameList, reportPath,commonName)
    print('测试报告已生成，请去以下路径提取：', reportName)
    log.logINFO('测试报告已生成，请去以下路径提取：'+str(reportName))


def run_List(commonName):

    # step 1：读取公共配置文件信息
    l = pre.gen_commonconfig(commonName)
    # step2：读取testsuit地址
    casePath = os.path.dirname(os.getcwd())+l['caseconfig']
    print(casePath)
    # step3: 读取testsuit
    testsuit = os.listdir(casePath)
    print(testsuit)
    lcase = l
    # step4：循环每个testcase
    for testcase in testsuit:
        if not os.path.isdir(testcase):
            print("*-------读取到案例："+testcase + "-------------*")
            log.logINFO("*-------读取到案例："+testcase + "-------------*")
            lcase['caseconfig'] = casePath + "\\"+ testcase
            # \\conf\\testsuit
            print('案例地址：'+lcase['caseconfig'])
            log.logINFO('案例地址：'+lcase['caseconfig'])
            run_single(lcase, commonName)
        else:
            print(testcase + "is not a valid case file!!!")
    se = send.Send()
    se.sendMultiUser()


if __name__ == '__main__':
    #命令输入参数
    commonName = sys.argv[1]
    # commonName='CommonBisheng.yaml'
    run_List(commonName)












