#!/usr/bin/env python
# coding:utf-8

import json
import mySpiders.utils.log as logging
from httpRequest import HttpRequest
from config import requst_distinct_url, requst_length_url, request_url, sync_last_md5_url

"""
requstDistinct          批量检测url是否已经存在
getCrawlRequestLength   获取待处理request个数
getCrawlRequest         获取spider_rules配置，可以同时更新last_md5校验码
syncLastMd5             同步last_md5校验码
"""


def requstDistinct(hashCode):
    try:
        http = HttpRequest()
        url = requst_distinct_url
        hashCode = ",".join(hashCode)
        body = {'field': hashCode}
        encryptFields = ['field']
        encryptFields = []
        response = http.setUrl(url).setBody(body).encrypt(encryptFields).post()
        res = json.loads(response)['data']
        if not res:
            return []
        return res
    except Exception, e:
        res = []
        logging.info('-----------%s-------' % e)
        return res


def getCrawlRequestLength():
    try:
        http = HttpRequest()
        url = requst_length_url
        response = http.setUrl(url).setBody({}).encrypt([]).post()
        res = json.loads(response)['data']
        if res == 'null':
            res = None
    except Exception, e:
        logging.info("-----%s-----" % e)
        return None
    return int(res)


def getCrawlRequest(params={}):

    try:
        http = HttpRequest()
        url = request_url
        response = http.setUrl(url).setBody(params).encrypt([]).post()
        res = json.loads(response)['data']
        if res == 'null':
            res = None
    except Exception, e:
        print e
        logging.info("-----%s-----" % e)
        return None
    return res


def syncLastMd5(params):

    try:
        http = HttpRequest()
        url = sync_last_md5_url
        response = http.setUrl(url).setBody(params).encrypt([]).post()
        res = json.loads(response)['data']
        if res == 'null':
            res = None
    except Exception, e:
        print e
        logging.info("-----%s-----" % e)
        return None
    return res

__all__ = ['requstDistinct', 'getCrawlRequestLength', 'getCrawlRequest', 'syncLastMd5']

# print requstDistinct(toMd5('http://www.ftchinese.com/story/001066870'))
# print getCrawlRequest()
