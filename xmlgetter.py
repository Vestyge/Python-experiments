# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 05:07:00 2022

@author: dream
"""

import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Input URL: ')
addr = urllib.request.urlopen(url, context=ctx)
data = addr.read()
cnt = 0;

# print(data.decode())
   
tree = ET.fromstring(data)
comments = tree.findall('comments/comment')
for item  in comments:
    cnt += int(item.find('count').text)
print(cnt)