#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author='Jingle,LEOMASTER.CO.LTD'

import os
import sys

path = os.getcwd()
sys.path.append(path)
import yaml


def read_yaml(yamlpath):
    f = open(yamlpath)
    l = yaml.load(f)
    return l

if __name__ == '__main__':
    rootpath = os.path.dirname(os.getcwd())
    yamlpath = rootpath + '\\conf\\testsuit\\QingTuiCall.yaml'
    l = read_yaml(yamlpath)
    print(l)

