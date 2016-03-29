#!/usr/bin/env python
# coding:utf8
import time
import json
import scrapy

from mySpiders.utils.httpRequest import HttpRequest
from scrapy.crawler import CrawlerProcess
from gevent.pool import Pool,Group
from mySpiders.spiders.XmlFeedSpider import XmlFeedSpider

SLEEP_TIMES = 60
MAX_POOL_NUM = 15


class SpiderPool(object):

    def __init__(self, size=None):
        if not size:
            size = MAX_POOL_NUM

        self.pool = Pool(size)
        # self.pool.start([])

    def runSpider(self):
        print "begin---runSpider-----"
        process = CrawlerProcess()
        process.crawl(XmlFeedSpider)
        process.start()
        print "end---runSpider-----"
        pass

    def add_handler(self):
        if self.pool.full():
            raise Exception('at maxinum pool size')
        else:
            self.pool.spawn(self.runSpider)

    def shutdown(self):
        self.pool.kill()


class RunSpider(object):

    def __init__(self, spiderPool):
        self.pool = spiderPool
        self.configArg = None
        self.sleepTimes = SLEEP_TIMES
        pass

    def run(self):
        # self.getSpiderConfig()
        self.runSpider()

    def runSpider(self):
        while True:
            try:
                self.pool.add_handler()
                self.pool.pool.join()
                # self.pool.add_handler(self.configArg)
            except Exception, e:
                print "-----------------"
                time.sleep(self.sleepTimes)
                continue
            break
        return True

    def getCrawlRequest():
        try:
            http = HttpRequest()
            url = 'http://www.babel.com/api/get-spider-rules/get'
            body = {'action': 'get', 'version': '1.1'}
            encryptFields = ['action', 'version']
            res = http.setUrl(url).setBody(body).encrypt(encryptFields).post()
            res = json.loads(res)['data']
            if res == 'null':
                res = None
        except Exception, e:
            print e
            return None
        finally:
            pass
        return res

    def getSpiderConfig(self):
        """获取爬虫配置项，若果redis为空，则休眠60s"""
        while True:
            spiderConfig = self.getCrawlRequest()
            if spiderConfig:
                break
            # log
            time.sleep(self.sleepTimes)

        self.configArg = spiderConfig
        return True


def main():
    spiderPool = SpiderPool()
    runSpider = RunSpider(spiderPool)
    while True:
        while True:
            runSpider.run()


def getCrawlRequest():
    try:
        http = HttpRequest()
        url = 'http://www.babel.com/api/get-spider-rules/get'
        body = {'action': 'get', 'version': '1.1'}
        encryptFields = ['action', 'version']
        res = http.setUrl(url).setBody(body).encrypt(encryptFields).post()
        res = json.loads(res)['data']
        if res == 'null':
            res = None
    except Exception, e:
        print e
        return None
    finally:
        pass
    return res

if __name__ == '__main__':
    main()
