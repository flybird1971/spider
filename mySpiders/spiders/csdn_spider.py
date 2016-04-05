#!/usr/bin/env python
# coding:utf-8

from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from mySpiders.items import CSDNItem
import time
import logging


class CSDNSpider(Spider):

    name = 'csdn_spider'
    download_delay = 1
    allowed_domain = ['blog.csdn.net']
    start_urls = [
        "http://blog.csdn.net/u012150179/article/details/11749017"
    ]

    def parse(self, response):
        with open('est--dat.json', 'a+') as f:
            f.write("eeeeeeeeeeeeeeeeeeeee--------" + str(time.time())+'\n')
        logging.info("eeeeeeeeeeeeeeeeeeeee--------" + str(time.time())+'\n')
        # print "eeeeeeeeeeeeeeeeeeeee--------".time.time()

        sel = Selector(response)

        item = CSDNItem()
        artile_url = str(response.url)
        artile_name = sel.xpath('//div[@id="article_details"]/div/h1/span/a/text()').extract()
        item['name'] = [n.encode('utf-8') for n in artile_name]
        item['url'] = artile_url.encode('utf-8')

        yield item

        # urls = sel.xpath('//li[@class="next_article"]/a/@href').extract()
        # for url in urls:
        #     print url
        #     url = "http://blog.csdn.net"+url
        #     print url
        #     yield Request(url,callback=self.parse)
