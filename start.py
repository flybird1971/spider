#!/usr/bin/env python
# coding:utf8
import redis
import time
from mySpiders.utils.httpRequest import HttpRequest
import json

SLEEP_TIMES = 60
spiderCount = {'max_run_spider': 10, 'current_run_spider': 0}


def getSpiderConfig(sleepTimes=SLEEP_TIMES):
    """获取爬虫配置项，若果redis为空，则休眠60s"""
    while True:
        spiderConfig = getCrawlRequest()
        if spiderConfig:
            break
        # log
        time.sleep(sleepTimes)

    return spiderConfig


def runSpider():

    while True:
        spiderConfig = getSpiderConfig()
        # scrapy crawl xmlfeedspider
        spiderCount['current_run_spider'] -= 1
        if spiderConfig['current_run_spider'] < 0:
            spiderConfig['current_run_spider'] = 0
        return True


def getCrawlRequest():
    try:
        http = HttpRequest()
        url = 'http://www.babel.com/api/get-spider-rules/get'
        body = {'action': 'get', 'version': '1.1'}
        encryptFields = ['action', 'version']
        res = http.setUrl(url).setBody(body).encrypt(encryptFields).post()
        res = json.loads(res)['data']
    except Exception, e:
        return None
    finally:
        pass
    return res

if __name__=='__main__':
    print getCrawlRequest()