#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author='Jingle,LEOMASTER.CO.LTD'

import os
import logging
import logging.config

# 统一读取配置文件
rootpath = os.path.dirname(os.getcwd())
logging.config.fileConfig(rootpath + '\conf\logger.conf')


# 打印debug日志
def logINFO(infoString):

    logger = logging.getLogger('example02')
    logger.info(infoString)


if __name__ == '__main__':
    infoString = 'This is a info String'
    errorString = 'This is a error String'
    for i in range(0, 3):
        logINFO(infoString)



