# -*- coding: utf-8 -*-
from scrapy.spiders import CSVFeedSpider

from spiders.items import SpidersItem


class TestcsvfeedSpider(CSVFeedSpider):
    name = 'testcsvfeed'
    allowed_domains = ['teste.csvfeed']
    start_urls = ['http://www.teste.csvfeed/feed.csv']
    # headers = ['id', 'name', 'description', 'image_link']
    # delimiter = '\t'

    # Do any adaptations you need here
    #def adapt_response(self, response):
    #    return response

    def parse_row(self, response, row):
        i = SpidersItem()
        #i['url'] = row['url']
        #i['name'] = row['name']
        #i['description'] = row['description']
        return i
