# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 04:08:33 2022

@author: dream
"""

import socket

url = input('Please input desired url: ');
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
count = 0;
headersend = 0; #finds position when page header ends and content begins

try:
    mysock.connect((url.split('/')[2], 80))

except:
    print('Incorrect URL')

else:
    cmd = ('GET ' + url + ' HTTP/1.0\r\n\r\n').encode()
    mysock.send(cmd)
    while True:
        data = mysock.recv(512)
        headerend = data.decode().find('\r\n\r\n')
        if headerend == -1: #later iterations without headerend
            count += len(data);
            if count <= 3000:
                print(data.decode(),end='')
        else: #first initialisation to find header position
            headersend = headerend+4;
            datas = data[headersend:]
            count += len(datas)
            if count <= 3000:
                print(data.decode()[headersend:],end='')
        if len(data) < 1:
            print("\nTotal number of characters: " + str(count))
            break


        
mysock.close()