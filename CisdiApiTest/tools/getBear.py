#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author='Jingle,LEOMASTER.CO.LTD'
import base64

access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaWQiOiJlMWJkYTM1YTA5MjA0YmMxOWE5OGFhNzA5NzY4ZDNmMCIsImV4cGlyZXMiOjE1MDc1OTc3MDQsInR5cGUiOiJjbGllbnQifQ.nsh_3t2NPsTpPIgqWlF38fjXdZRQajXmnrNRy5FG4kQ'
domainId = '2646d8386de9418ea2ab130c3b567bc2'

tail = base64.b64encode(domainId)
bear = 'Bearer ' + access_token + '.' + tail
print ("Bearer长这样：",bear)
