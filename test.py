#!/usr/bin/env python
# coding:utf8

import time
from scrapy.crawler import CrawlerProcess
from mySpiders.spiders.csdn_spider import CSDNSpider
from mySpiders.utils.http import getCrawlRequest, requstDistinct


def test():
    process = CrawlerProcess()
    process.crawl(CSDNSpider)
    process.crawl(CSDNSpider)
    process.start()  # the script will block here until all crawling jobs are finished

    print "=============================="
    time.sleep(1)


# test()

# param = {'last_md5': 'd78419dfd961ca6c24a80b6f7800d7e5', 'id': '1'}
print getCrawlRequest()

# listd = [
#     'aaaaaaaaaaaaa221e1e23',
#     'aaaaaaaaaaaaa11e1',
#     'aaaaaaaaaaaaa2e11',
#     'aaaaaaaaaaaaa33e11',
# ]
# t = [x.encode('utf-8') for x in listd]
# print requstDistinct(listd)
# td = {
#     'a': 'a21',
#     'b': 'cc'
# }
# l = ['a']

# print td
# for i, unique in enumerate(l):
#     print i, unique
#     del(td[unique])
# print td
