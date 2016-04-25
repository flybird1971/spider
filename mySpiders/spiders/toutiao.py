# -*- coding: utf-8 -*-
# import re

from scrapy.http import Request
from mySpiders.spiders.MyBaseSpider import MyBaseSpider
import mySpiders.utils.log as logging
from mySpiders.items import ToutiaoItem
import re


class JokeSpider(MyBaseSpider):

    name = 'toutiao.io'

    start_urls = [
        'http://toutiao.io/explore?page=1'
    ]

    num_pattern = re.compile(r'\d+', re.M | re.S)

    custom_settings = {
        'ITEM_PIPELINES': {
            'mySpiders.pipelines.ToutiaoPipeline': 1
        }
    }

    def start_requests(self):

        self.titleXpath = '//*[@id="main"]/div/ul/li/h4/a/text()'
        self.urlXpath = '//*[@id="main"]/div/ul/li/div/span[1]/a/@href'
        self.shareNumXpath = '//*[@id="main"]/div/ul/li/div/span[2]/text()'
        self.rssNumXpath = '//*[@id="main"]/div/ul/li/div/span[3]/text()'
        self.next_request_url = '//li[@class="next"]/a/@href'
        self.max_deepth = 500

        return [Request('http://toutiao.io/explore?page=1', callback=self.parse, dont_filter=True)]

    def parse(self, response):

        item = ToutiaoItem()
        item['title'] = self.safeParse(response, self.titleXpath, True)
        item['url'] = [self.appendDomain(i, response.url) for i in self.safeParse(response, self.urlXpath, True)]

        item['share_num'] = []
        for i in self.safeParse(response, self.shareNumXpath, True):
            num = 0
            r = self.num_pattern.search(i)
            if r:
                num = r.group()
            item['share_num'].append(num)

        item['rss_num'] = []
        for i in self.safeParse(response, self.rssNumXpath, True):
            num = 0
            r = self.num_pattern.search(i)
            if r:
                num = r.group()
            item['rss_num'].append(num)

        yield item

        # 获取下一列表页url
        for request in self.getNextListPageUrl(response):
            yield request
