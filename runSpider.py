#!/usr/bin/env python
# coding:utf8

import mySpiders.utils.log as logging
from scrapy.crawler import CrawlerProcess
from mySpiders.spiders.CommonXmlFeed import XmlFeedSpider
from mySpiders.utils.http import getCrawlNoRssRequestLength
from scrapy.utils.project import get_project_settings
from config import SPIDER_MAX_POOL_NUM


class RunSpider(object):

    def __init__(self, size=None):

        if not size:
            size = SPIDER_MAX_POOL_NUM
        self.size = size
        self.process = None
        self.runNum = 0

    def initSpider(self):
        if not self.process:
            self.process = CrawlerProcess(get_project_settings())

        self.process.crawl(XmlFeedSpider)
        self.runNum += 1

    def runSpider(self):

        self.runNum = 0
        self.process.start()

    def run(self):
        while True:
            num = getCrawlNoRssRequestLength()
            logging.info("-----need deal request num-----%s " % num)
            if not num:
                if self.runNum >= 1:
                    logging.info("*************tt*************size:-%s--runNum:--%s--" % (self.size, self.runNum))
                    self.runSpider()
                break
            else:
                self.initSpider()
                if self.runNum >= self.size:
                    logging.info("--size:-%s--runNum:--%s--" % (self.size, self.runNum))
                    self.runSpider()
                    break


def main():
    try:
        runSpider = RunSpider()
        runSpider.run()
        logging.info("---runSpider end-----------")
    except Exception, e:
        logging.info("---runSpider main function Exception : %s-----" % e)

if __name__ == '__main__':
    main()
