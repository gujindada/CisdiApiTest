#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author='Jingle,LEOMASTER.CO.LTD'

import re
from Assert import MultiAssert as multiAssert


class Assert(object):
    def __init__(self):
        pass

    def get_assertResult(self, assertDict={'assertKey': None,'assertContent': None} , res_content={}):
        '''
            assertDict: 存放断言配置的字典
            res_content:实际返回的body
            :return result 返回字符串判定结果"pass"、"error"
        '''
        # 定义存储
        assertResultList = []
        realValueList = []
        # 如果不进行任何校验
        if assertDict['assertKey'] == None and assertDict['assertContent'] == None:
            result = "not check"
            d = "No result"
            assertResultList.append(result)
            realValueList.append(d)
        else:
            assertKeyList = assertDict['assertKey']
            assertContentList = assertDict['assertContent']

            # 默认实际校检值是全局返回的json串
            d = res_content
            for i in range(len(assertKeyList)):
                try:
                    assertKey = assertKeyList[i]
                    assertContent = assertContentList[i]
                    # 判断是否为嵌套单值断言
                    if '--' in assertKey:
                        keylist = assertKey.split('--')
                        key = keylist[0]
                        d = res_content[key]
                        for i2, key in enumerate(keylist):
                            if i2 >= 1:
                                # 从长度足够的数组中取下标
                                if type(d)==list and re.compile('^[0-9]*$').match(key) and len(d)>int(key):
                                    d = d[int(key)]
                                # 如果key存在于检索范围中
                                elif type(d)==dict and d.has_key(key):
                                    d = d[key]
                                else:
                                    d = 'Out range index of List,Or the key is not exist '

                            i += 1
                    # 非嵌套单值断言
                    elif assertKey is not None:
                        d = res_content[assertKey]

                    # 断言比对
                    result = multiAssert.multiAssert(d, assertContent)
                    assertResultList.append(result)
                    realValueList.append(d)
                except:
                    raise
                    result = 'error'
                    d = 'No result'
                    assertResultList.append(result)
                    realValueList.append(d)

        return assertResultList, realValueList


if __name__ == '__main__':
    pass









