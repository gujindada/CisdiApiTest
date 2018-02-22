#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author='Jingle,LEOMASTER.CO.LTD'

import os
from utils import yamlhandler


# 读取公共配置信息
def gen_commonconfig(commonName):
    # 读取公共配置信息
    rootpath = os.path.dirname(os.getcwd())
    configpath = rootpath + '\conf\\'+commonName
    l = yamlhandler.read_yaml(configpath)
    return l


# 读取案例配置信息
def gen_caseconfig(l):
    rootpath = os.path.dirname(os.getcwd())
    casepath = l['caseconfig']
    lc = yamlhandler.read_yaml(casepath)
    #提取公共域名
    domain = l['domain']
    return lc, domain


def gen_caseinfo(lc, domain):
    # 提取断言配置
    assertinfolist = []
    caseinfolist = []
    lclist = lc['test']
    lcnamelist = lc['name']
    for i,val in enumerate(lclist):
        assertval = val[lcnamelist[i]]['assert']
        assertinfolist.append(assertval)
        # 提取纯案例信息
        del val[lcnamelist[i]]['assert']
        caseval = val[lcnamelist[i]]
        url = caseval['url']
        caseval['url'] = domain + url
        caseinfolist.append(caseval)
    return caseinfolist, assertinfolist, lcnamelist


if __name__ == '__main__':
    l = gen_commonconfig(commonName='commonBisheng.yaml')
    print(l)
    '''lc,domain = gen_caseconfig(l)
    print (lc)
    caseinfolist, assertinfolist, lcnamelist = gen_caseinfo(lc, domain)
    print(caseinfolist)
    print(assertinfolist)'''

