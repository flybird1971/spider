#!/usr/bin/env python
# coding:utf8

import time
import logging
from scrapy.crawler import CrawlerProcess
# from mySpiders.spiders.XmlFeedSpider import XmlFeedSpider
from mySpiders.spiders.CommonXmlFeed import XmlFeedSpider

from mySpiders.utils.http import getCrawlRequestLength
# from mySpiders.utils.httpRequest import HttpRequest
from scrapy.utils.project import get_project_settings
# from scrapy.conf import settings


SLEEP_TIMES = 6
MAX_POOL_NUM = 3


class RunSpider(object):

    def __init__(self, size=None):
        if not size:
            size = MAX_POOL_NUM
        self.size = size
        self.process = None
        # self.process = CrawlerProcess(get_project_settings())
        self.isRun = True
        self.isNew = True
        self.runNum = 0

    def initSpider(self):
        if not self.process:
            logging.info("---process---%s--" % self.process)            
            self.process =  CrawlerProcess(get_project_settings())

        logging.info("begin---runSpider-----")
        self.process.crawl(XmlFeedSpider)
        self.runNum += 1
        logging.info("end---runSpider-----")

    def runSpider(self):
        # self.isRun = True
        # if self.isRun and self.isNew:
        logging.info("--runnig-process---%s--" % self.process)     
        self.runNum = 0
        self.process.start()
        # self.process.stop()
        # del self.process
        # self.process = None
        # self.isRun = False
        # self.isNew = False
        
        

    def run(self):
        while True:
            num = getCrawlRequestLength()
            logging.info("-----need deal request num-----%s " % num)
            if not num:
                if self.runNum >= 1:
                    logging.info("*************tt*************size:-%s--runNum:--%s--" % (self.size,self.runNum))  
                    self.runSpider()
                    self.process = None
                logging.info("-----sleep %s seconds--spiderNUM %s-- " % (SLEEP_TIMES,num))
                time.sleep(SLEEP_TIMES)
                continue
            else:
                self.initSpider()
                if self.runNum >= self.size:
                    logging.info("--size:-%s--runNum:--%s--" % (self.size,self.runNum))   
                    self.runSpider()
                    self.process = None



def main():
    
    while True:
        try:
            runSpider = RunSpider()
            runSpider.run()
        except Exception, e:
            logging.info("---while Exception : %s-----" % e )

if __name__ == '__main__':
    main()
    
