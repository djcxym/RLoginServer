#!/usr/bin/env python
#-*- coding:utf-8 -*-

from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from DBManager import *
from ResponseCode import *
import json
import urlparse
import cgi
import threading
import urllib
import base64
import os

class TestHTTPHandler(BaseHTTPRequestHandler):  
    def do_GET(self): 
        pass
            
    def do_POST(self):
        print 'POST connection from ',self.client_address
        parsed_path = urlparse.urlparse(self.path)
        print threading.currentThread().getName()
        if self.path == '/register':
            handleRegister(self)
        if self.path == '/login': 
            handleLogin(self)

def handleRegister(handler):
    ctype, pdict = cgi.parse_header(handler.headers['content-type'])
    if ctype == 'application/json':
        length = int(handler.headers['content-length'])
        registerInfo = json.loads(handler.rfile.read(length))
        if !registerInfo.has_key('Name')||!registerInfo.has_key('Password'):
            handler.send_error(412, "Key missing.")
            return

        name = registerInfo['Name']
        sql = 'SELECT Name FROM UserInfo WHERE Name = ' + "'" + name + "'"
        fetchResult = fetchAll(sql)
        # 用户名已存在
        if fetchResult is not None:
            sendResponse(handler,registerExists)
            return

        avatarUrl = ''#保存头像
        if registerInfo.has_key('avatar'):
            avatarFile = '../avatar/' + name + '.jpeg'
            print avatarFile
            avatarData = registerInfo['avatar'];
            f = open(avatarFile,'wb')
            f.write(base64.b64decode(avatarData))
            f.close()
            avatarUrl = avatarFile[1:]

        userInfo = [registerInfo['Name'],registerInfo['Password'],avatarUrl];
        insert(userInfo)
        sendResponse(handler,registerSuccess)
    else:
        handler.send_error(412, "Only json is supported.")
        return

def handleLogin(handler):
    ctype, pdict = cgi.parse_header(handler.headers['content-type'])
    if ctype == 'application/json':
        length = int(handler.headers['content-length'])
        loginInfo = json.loads(handler.rfile.read(length))
        # print loginInfo
        if !loginInfo.has_key('Name')||!loginInfo.has_key('Password'):
            handler.send_error(412, "Key missing.")
            return
        name = loginInfo['Name']
        passEntered = loginInfo['Password']
        sql = 'SELECT Password FROM UserInfo WHERE Name = ' + "'" + name + "'"
        fetchResult = fetchAll(sql)
        if fetchResult is not None:
            passStored = fetchResult[0][0]
            if passEntered == passStored:
                sendResponse(handler,loginSuccess)
            else:
                sendResponse(handler,loginPassError)
        else:
            sendResponse(handler,loginNotExists)
    else:
        handler.send_error(412, "Only json data is supported.")
        return
    
def sendResponse(handler,data):
    handler.send_response(200)
    handler.send_header('Content-type', 'application/json')
    handler.end_headers()
    handler.wfile.write(json.dumps(data))

class ThreadedHTTPServer(ThreadingMixIn,HTTPServer):
    pass 

def start_server(port):  
    http_server = ThreadedHTTPServer(('10.9.36.25', int(port)), TestHTTPHandler)  
    http_server.serve_forever()  

if __name__ == '__main__':
    createTable()
    start_server(12345)