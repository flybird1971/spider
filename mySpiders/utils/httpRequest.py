#!/usr/bin/env python
# coding:utf-8
"""
pip install rsa
"""

import urllib
import urllib2
import base64
import md5
import datetime
import json
from config import ENCRYPT_MD5_KEY


class HttpRequest(object):

    action = 'get'
    version = '1.1'

    def __init__(self, url='', requestType='post'):
        self.url = url
        self.type = requestType
        self.body = {}
        self.timeout = None

    def setUrl(self, url):
        self.url = url
        return self

    def getUrl(self):
        return self.url

    def setRequestType(self, requestType):
        self.requestType = requestType
        return self

    def getRequestType(self):
        return self.requestType

    def setBody(self, body):
        self.body = body
        return self

    def getBody(self):
        return self.body

    def post(self):
        if not self.url:
            raise Exception('url must not emptye')

        self.setRequestType('post')
        return self.send()

    def get(self):
        if not self.url:
            raise Exception('url must not emptye')

        self.setRequestType('get')
        self.url = self.url + '?' + urllib.urlencode(self.body)
        return self.send()

    def send(self):
        try:
            if self.requestType == 'post':
                self.body = urllib.urlencode(self.body)
                print self.url,self.body
                req = urllib2.Request(url=self.url, data=self.body)
            else:
                print self.url
                req = urllib2.Request(self.url)

            if self.timeout:
                response = urllib2.urlopen(req, timeout=self.timeout)
            else:
                response = urllib2.urlopen(req)

            response = response.read()
            return response
        except (urllib2.HTTPError, Exception), e:
            print e

    def toMd5(self, data):
        m = md5.new()
        m.update(data)
        return m.hexdigest()

    def getDate(self):
        return datetime.datetime.now().strftime('%Y-%m-%d')

    def setTimeout(self, timeout):
        self.timeout = timeout

    def encrypt(self, encryptFields=[]):
        self.body['action'] = HttpRequest.action
        self.body['version'] = HttpRequest.version
        encryptFields.append('action')
        encryptFields.append('version')
        md5KeyPrefix = self.toMd5(self.getDate())[3:10]
        md5KeySubfix = self.toMd5(self.getDate())[12:25]
        self.md5Key = self.toMd5(md5KeyPrefix + ENCRYPT_MD5_KEY + md5KeySubfix)
        for i, key in enumerate(encryptFields):
            self.body[key] = self.__encrypt(self.body[key])
        return self

    def __encrypt(self, data):
        m = md5.new()
        m.update(self.md5Key)
        key = m.hexdigest()
        x = 0
        length = len(data)
        l = len(key)
        char = strs = ''
        for i in xrange(0, length):
            if (x == l):
                x = 0
            char += key[x]
            x += 1
            i += 1
        for i in xrange(0, length):
            strs += chr(ord(data[i]) + (ord(char[i])) % 256)
            i += 1
        return base64.b64encode(strs)

__all__ = ['HttpRequest']

if __name__ == '__main__':

    http = HttpRequest()
    url = 'http://www.babel.com/api/cluster-requst-distinct/index'
    body = {'field': 'abcdefgbe'}
    encryptFields = ['field']
    res = http.setUrl(url).setBody(body).encrypt(encryptFields).post()
    print json.loads(res)['data']
