#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author='Jingle,LEOMASTER.CO.LTD'

import os
import xlwt
import time


# 初始化报告表格
def create_report(reportDict, casenameList, reportpath, commonName):
    '''
        :param reportDict: 报告字典
        :param casenameList: 接口执行顺序
        :param reportPath: 报告路径
        :return:
    '''
    rootpath = os.path.dirname(os.getcwd())
    # 获取当前时间戳
    timeformat = '%Y-%m-%d %X'
    t = time.strftime(timeformat,time.localtime()).replace(':', '-')
    filename = rootpath + reportpath + '\\' + commonName + '_Result' + t + '.xls'
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('Test Result')
    # 初始化列名称
    worksheet.write(0, 0, label='接口名称')
    worksheet.write(0, 1, label='请求url')
    worksheet.write(0, 2, label='接口发送数据')
    worksheet.write(0, 3, label='实际接收数据')
    worksheet.write(0, 4, label='校检字段')
    worksheet.write(0, 5, label='校检结果')
    worksheet.write(0, 6, label='校检字段预期值')
    worksheet.write(0, 7, label='校检字段实际值')
    worksheet.write(0, 8, label='接口测试时间')
    worksheet.write(0, 9, label='接口重跑次数')
    for row in range(len(casenameList)):
        casename = casenameList[row]
        subReportDict = reportDict[casename]
        worksheet.write(row+1, 0, label=str(subReportDict['ApiName']))
        worksheet.write(row+1, 1, label=str(subReportDict['url']))
        worksheet.write(row+1, 2, label=str(subReportDict['requestData']))
        worksheet.write(row+1, 3, label=str(subReportDict['realReceptData']))
        worksheet.write(row+1, 4, label=str(subReportDict['checkKey']))
        worksheet.write(row+1, 5, label=str(subReportDict['checkResult']))
        worksheet.write(row+1, 6, label=str(subReportDict['expectValue']))
        worksheet.write(row+1, 7, label=str(subReportDict['realValue']))
        worksheet.write(row+1, 8, label=subReportDict['time'])
        worksheet.write(row+1, 9, label=subReportDict['repeatTimes'])
        row += 1
    workbook.save(filename)
    return filename






