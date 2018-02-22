#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author='Jingle,LEOMASTER.CO.LTD'


def multiAssert(expectvalue, assertContentDict):
    result = None
    multiresult = {'value': 'not check',
                   'length': 'not check',
                   'notNone': 'not check',
                   'valueType': 'not check'}

    if assertContentDict is not None:
        # 非空判定
        if assertContentDict['notNone'] is not None and expectvalue is not None:
            multiresult['notNone'] = 'pass'
        elif assertContentDict['notNone'] is not None and expectvalue is None:
            multiresult['notNone'] = 'fail'
        # 长度判断
        if assertContentDict['length'] is not None and \
                (len(assertContentDict['value']) == len(expectvalue)):
            multiresult['length'] = 'pass'
        elif assertContentDict['length'] is not None and \
                (len(assertContentDict['value']) != len(expectvalue)):
            multiresult['length'] = 'fail'
        # 数据类型判断
        if assertContentDict['valueType'] is not None and \
                (str(type(expectvalue)) == assertContentDict['valueType']):
            multiresult['valueType'] = 'pass'
        elif assertContentDict['valueType'] is not None and \
                (str(type(expectvalue)) != assertContentDict['valueType']):
            multiresult['valueType'] = 'fail'
        # 值判断
        if assertContentDict['value'] is not None and \
                        assertContentDict['value'] == expectvalue:
            multiresult['value'] = 'pass'
        elif assertContentDict['value'] is not None and \
                        assertContentDict['value'] != expectvalue:
            multiresult['value'] = 'fail'

        # 遍历每个维度的判定结果，给出最终判定结论
        notCheckNum = 0
        keyNum = 0
        preResult = None
        for key in multiresult:
            if multiresult[key] == 'not check':
                notCheckNum += 1
            if multiresult[key] == 'fail':
                preResult = 'fail'
            keyNum += 1
        if notCheckNum == keyNum:
            result = 'not check'
        elif preResult == 'fail':
            result = 'fail'
        else:
            result = 'pass'

    # 如果断言结果本身为空，直接给出未判断结论
    else:
        result = 'not check'

    return result
