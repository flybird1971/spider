#!/usr/bin/env python
# coding:utf8

import time
import logging
import json
from scrapy.crawler import CrawlerProcess
from mySpiders.spiders.XmlFeedSpider import XmlFeedSpider
from mySpiders.utils.httpRequest import HttpRequest
from scrapy.conf import settings


SLEEP_TIMES = 6
MAX_POOL_NUM = 15


class RunSpider(object):

    def __init__(self, size=None):
        if not size:
            size = MAX_POOL_NUM
        self.size = size
        self.process = CrawlerProcess(settings)
        self.isRun = True
        self.isNew = True
        self.runNum = 0

    def initSpider(self):
        logging.info("begin---runSpider-----")
        self.process.crawl(XmlFeedSpider,**self.spiderConfig)
        logging.info("end---runSpider-----")

    def runSpider(self):
        self.isRun = True
        if not self.isNew:
            self.process =  CrawlerProcess(settings)

        if self.isRun and self.isNew:
            self.process.start()
            self.isRun = False
            self.isNew = False
        self.runNum = 0

    def run(self):
        while True:
            self.spiderConfig = self.getCrawlRequest()
            # logging.info("-----spiderConfig-----%s " % self.spiderConfig)
            if not self.spiderConfig:
                if self.runNum < 1:
                    logging.info("-----sleep %s seconds---- " % SLEEP_TIMES)
                    time.sleep(SLEEP_TIMES)
                    continue
                self.runSpider()
            else:
                self.initSpider()
                self.runNum += 1
                if self.runNum >= self.size:
                    self.runSpider()

    def getCrawlRequest(self):
        
        try:
            http = HttpRequest()
            url = 'http://www.babel.com/api/get-spider-rules/get'
            body = {'action': 'get', 'version': '1.1'}
            encryptFields = ['action', 'version']
            res = http.setUrl(url).setBody(body).encrypt(encryptFields).post()
            res = json.loads(res)['data']
            # logging.info("-----%s-----" % res)
            if res == 'null':
                res = None
        except Exception, e:
            logging.info("-----%s-----" % e)
            return None
        finally:
            pass
        return res



def main():
    runSpider = RunSpider()
    while True:
        try:
            runSpider.run()
        except Exception, e:
            logging.info("---while Exception : %s-----" % e )

if __name__ == '__main__':
    main()
