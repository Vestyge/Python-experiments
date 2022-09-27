# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 01:45:43 2022

@author: dream
"""
import urllib.request

url = input('Please input desired url: ');
try:
    fhand = urllib.request.urlopen(url)
except:
    print('Incorrect URL')
else:
    count = 0;
    for line in fhand:
        data = line.decode().strip()
        count += len(line);
        if count <= 3000:
            print(data)
    print("\nTotal number of characters: " + str(count))
            
    
