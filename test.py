#!/usr/bin/env python
# coding:utf8

import time
from scrapy.crawler import CrawlerProcess
from mySpiders.spiders.csdn_spider import CSDNSpider
from mySpiders.utils.http import getCrawlRequest, requstDistinct, syncLastMd5, syncCrawlInfos
from mySpiders.utils.hash import toMd5
from mySpiders.sql.syncCrawlInfos import SyncCrawlInfos


def test():
    process = CrawlerProcess()
    process.crawl(CSDNSpider)
    process.crawl(CSDNSpider)
    process.start()  # the script will block here until all crawling jobs are finished

    print "=============================="
    time.sleep(1)


# test()

param = {'last_md5': toMd5(str(time.time())),
         'id': '1'}
# print syncLastMd5(param)
# print getCrawlRequest()

param = [{'4bbce00021506aecf54ba5884a415b16': 'http://blog.csdn.net/hj7jay/article/details/51148995'},
         {'b158d4b6473444ebfbaa2969c99c9e13': 'http://blog.csdn.net/hj7jay/article/details/51149155'},
         {'8d5bba3e45d473946872fc9c5afb94db': 'http://blog.csdn.net/hj7jay/article/details/51149167'},
         {'7b8efef578dcb2c1fc5ecf5490bc60d5': 'http://blog.csdn.net/hj7jay/article/details/51149227'},
         {'2b56b1e675b88d62db17dffa7171068b': 'http://blog.csdn.net/hj7jay/article/details/51149268'},
         {'3c3aed33445faba46168e0b83b5992e8': 'http://blog.csdn.net/hj7jay/article/details/51149207'},
         {'a068fd93771ed6f885294ee6b0069a50': 'http://blog.csdn.net/hj7jay/article/details/51149192'},
         {'56fb1745506c47314b95e5f8a6839bbc': 'http://blog.csdn.net/hj7jay/article/details/51149049'},
         {'18ddd7f50ef05e770663b7e531536284': 'http://blog.csdn.net/hj7jay/article/details/51149026'},
         {'615f5b11f490d968b78bf2bfa371ac9b': 'http://blog.csdn.net/hj7jay/article/details/51149077'},
         {'d28695543dbbc826b31311cf7f6f42b0': 'http://blog.csdn.net/hj7jay/article/details/51149040'},
         {'bcc18575606f09054b091f9e8ab89bb1': 'http://blog.csdn.net/hj7jay/article/details/51158756'},
         {'1ff59d7e6df00fc6320f7efa82c59a53': 'http://blog.csdn.net/hj7jay/article/details/51149132'},
         {'a809d74ec1fdb7b53c69e87db7a0f8d1': 'http://blog.csdn.net/hj7jay/article/details/51149181'}
         ]
# print requstDistinct(param.keys())
# print syncCrawlInfos(param)

# t = SyncCrawlInfos()
# t.index()

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
