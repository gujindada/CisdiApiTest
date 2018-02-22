#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author='Jingle,LEOMASTER.CO.LTD'

import json


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True
