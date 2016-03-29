#!/usr/bin/env python
# coding:utf-8

from scrapy.spiders import Spider
from scrapy.http import Request
from mySpiders.items import BsbdjItem
import re


class BsbdjSpider(Spider):

    regex = re.compile(r'([/\\])?[0-9]{1,5}$')

    name = 'www.budejie.com'

    allowed_domains = ['budejie.com']

    # download_delay = 1

    start_urls = [
        'http://www.budejie.com/new-video/',
        'http://www.budejie.com/new-pic/',
        'http://www.budejie.com/new-text/',
        'http://www.budejie.com/new-audio/',
    ]

    def parse(self, response):

        sels = response.xpath('/html/body/div[2]/div/div[1]/div[1]/div[2]/ul/li')
        for sel in sels:
            item = BsbdjItem()
            item['name'] = [n.encode('utf-8') for n in sel.xpath('div[2]/div[1]/text()').extract()]
            item['url'] = [(self.name + url).encode('utf-8')
                           for url in sel.xpath('div[3]/div[3]/ul/li[3]/a/@href').extract()]
            yield item

        newUrl = response.xpath('/html/body/div[2]/div/div[1]/div[2]/div/a[@class="z-crt"]/@href').extract()
        pageNum = int(newUrl[0]) + 1
        newUrl = self.regex.sub(r'\1', response.url) + str(pageNum)
        yield Request(newUrl, callback=self.parse)
