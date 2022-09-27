# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 05:28:00 2022

@author: dream
"""

import json
import urllib.request, urllib.parse, urllib.error
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Input URL: ')
addr = urllib.request.urlopen(url, context=ctx)
data = addr.read()
info = json.loads(data)
cnt = 0;

print('User count:', len(info["comments"]))

for item in info["comments"]:
    # print('Name', item['name'])
    # print('Id', item['id'])
    # print('Attribute', item['x'])
    cnt += item['count']
print(cnt)