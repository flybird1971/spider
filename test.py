#!/usr/bin/env python
# coding:utf8

import time
from scrapy.crawler import CrawlerProcess
from mySpiders.spiders.csdn_spider import CSDNSpider


def test():
    process = CrawlerProcess()
    process.crawl(CSDNSpider)
    process.crawl(CSDNSpider)
    process.start()  # the script will block here until all crawling jobs are finished

    print "=============================="
    time.sleep(1)


test()
