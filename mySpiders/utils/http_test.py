#!/usr/bin/env python
# coding:utf-8
"""
http请求类
    目前只支持get，post两种方式

demo:
    http = HttpRequest()
    url = 'http://www.baidu.com/index'  #请求url

    #post or get 数据
    body = {
        'field_1': 'value_1',
        'field_2': 'value_2',
        ......
    }

    #要加密参数
    encryptFields = [
        'encrpy_field_1',
        'encrpy_field_2',
        ......
    ]
    res = http.setUrl(url).setBody(body).encrypt(encryptFields).post()

    # Content-Encoding:gzip 要求post数据进行gzip压缩
    # Accept-Encoding:gzip  要求response响应进行gzip压缩
    headerDict = {'Content-Encoding':'gzip','Accept-Encoding':"gzip"}
    res = http.setUrl(url).setBody(body).setHeader(headerDict).encrypt(encryptFields).post()

    res = http.setUrl(url).setBody(body).encrypt(encryptFields).get()

"""

import urllib
import urllib2
import base64
import md5
import datetime
import json
import StringIO, gzip


class HttpRequest(object):
    """http 请求类，支持get or post
       可以设置header，进行gzip压缩或解压缩
    """

    def __init__(self, url='', requestType='post'):
        self.url = url
        self.type = requestType
        self.body = {}
        self.timeout = None
        self.headerDict = {}

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
            raise Exception('url must not empty !')

        self.setRequestType('post')
        return self.send()

    def get(self):
        if not self.url:
            raise Exception('url must not empty!')

        self.setRequestType('get')
        self.url = self.url + '?' + urllib.urlencode(self.body)
        return self.send()

    def setHeader(self,headerDict):
        """设置请求头"""

        self.headerDict = headerDict
        return self

    def appendHeader(self,req):
        """将头信息追加到request请求头部"""

        for field in self.headerDict:
            req.add_header(field,self.headerDict[field])
        return self

    def send(self):
        try:
            if self.requestType == 'post':
                self.body = urllib.urlencode(self.body)
                req = urllib2.Request(url=self.url, data=self.body)
            else:
                req = urllib2.Request(self.url)

            self.appendHeader(req)

            if self.timeout:
                response = urllib2.urlopen(req, timeout=self.timeout)
            else:
                response = urllib2.urlopen(req)

            response = response.read()
            if self.headerDict.get('Accept-Encoding',None) == 'gzip':
                compressedstream = StringIO.StringIO(response)
                gziper = gzip.GzipFile(fileobj=compressedstream)
                response = gziper.read()   # 读取解压缩后数据

            return response
        except (urllib2.HTTPError, Exception), e:
            print e

    def toMd5(self, data):
        """md5加密"""

        m = md5.new()
        m.update(data)
        return m.hexdigest()

    def getDate(self):
        """获取当前时间"""

        return datetime.datetime.now().strftime('%Y-%m-%d')

    def setTimeout(self, timeout):
        """超时设置"""

        self.timeout = timeout

    def encrypt(self, encryptFields=[]):
        """指定加密字段"""

        for field in encryptFields:
            if field not in self.body.keys():
                raise  Exception('encrypt field %s not exists!' % field )
            self.body[field ] = self.__encrypt(self.body[field ])
        return self

    def __encrypt(self, data):
        """具体加密逻辑 """

        # 此处代码隐藏
        return base64.b64encode(data)

__all__ = ['HttpRequest']

if __name__ == '__main__':

    http = HttpRequest()
    url = 'http://blog.csdn.net/other/index.html'  #请求url

    #post or get 数据
    body = {
        'field_1': 'value_1',
        'field_2': 'value_2',
    }

    #要加密参数
    encryptFields = [
        'field_1',
        'field_2',
    ]
    #res = http.setUrl(url).setBody(body).encrypt(encryptFields).post()

    # Content-Encoding:gzip 要求post数据进行gzip压缩
    # Accept-Encoding:gzip  要求response响应进行gzip压缩
    headerDict = {
        'Content-Encoding':'gzip',
        'User-Agent' : 'Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
    }
    #res = http.setUrl(url).setBody(body).setHeader(headerDict).encrypt(encryptFields).post()
    #print res
    res = http.setUrl(url).setBody(body).setHeader(headerDict).encrypt(encryptFields).get()
    print res