#!/usr/bin/env python
# coding:utf-8

import json
import mySpiders.utils.log as logging
from httpRequest import HttpRequest
from mySpiders.utils.hash import toMd5
from config import (requst_distinct_url, requst_rss_length_url,
                    request_rss_url, requst_norss_length_url, request_norss_url,
                    sync_last_md5_url, sync_crawl_infos_url)


"""
requstDistinct                  批量检测url是否已经存在
getCrawlRssRequestLength        获取待处理rss类型 request个数
getCrawlRssRequest              获取rss类型spider_rules配置，可以同时更新last_md5校验码
getCrawlNoRssRequestLength      获取待处理rss类型 request个数
getCrawlNoRssRequest            获取rss类型spider_rules配置，可以同时更新last_md5校验码
syncLastMd5                     同步last_md5校验码
syncCrawlInfos                  同步数据到线上
"""


def requstDistinct(hashCode):
    try:
        http = HttpRequest()
        url = requst_distinct_url
        hashCode = ",".join(hashCode)
        body = {'field': hashCode}
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


def getCrawlRssRequestLength():
    try:
        http = HttpRequest()
        url = requst_rss_length_url
        response = http.setUrl(url).setBody({}).encrypt([]).post()
        res = json.loads(response)['data']
        if res == 'null':
            res = None
    except Exception, e:
        logging.info("-----%s-----" % e)
        return None
    return int(res)


def getCrawlRssRequest(params={}):

    try:
        http = HttpRequest()
        url = request_rss_url
        response = http.setUrl(url).setBody(params).encrypt([]).post()
        res = json.loads(response)['data']
        if res == 'null':
            res = None
    except Exception, e:
        print e
        logging.info("-----%s-----" % e)
        return None
    return res


def getCrawlNoRssRequestLength():
    try:
        http = HttpRequest()
        url = requst_norss_length_url
        response = http.setUrl(url).setBody({}).encrypt([]).post()
        res = json.loads(response)['data']
        if res == 'null':
            res = None
    except Exception, e:
        logging.info("-----%s-----" % e)
        return None
    return int(res)


def getCrawlNoRssRequest(params={}):

    try:
        http = HttpRequest()
        url = request_norss_url
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


def syncCrawlInfos(dataList):

    try:
        http = HttpRequest()
        http.setTimeout(900)
        url = sync_crawl_infos_url
        sqlList = json.dumps(dataList)
        body = {'sql': sqlList, 'checksum': toMd5(sqlList)}
        encryptFields = []
        headerDict = {'Content-Encoding':'gzip','Accept-Encoding':"gzip"}
        response = http.setUrl(url).setBody(body).setHeader(headerDict).encrypt(encryptFields).post()
        res = json.loads(response)['data']
        if not res:
            return []
        return res
    except Exception, e:
        res = []
        logging.info('-----------%s-------' % e, True)
        return res


__all__ = [
    'requstDistinct',
    'getCrawlRssRequestLength',
    'getCrawlRssRequest',
    'getCrawlNoRssRequestLength',
    'getCrawlNoRssRequest',
    'syncLastMd5',
    'syncCrawlInfos'
]

# print requstDistinct(toMd5('http://www.ftchinese.com/story/001066870'))
# print getCrawlRequest()
# print syncCrawlInfos()
