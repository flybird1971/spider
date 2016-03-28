# -*- coding: utf-8 -*-
import scrapy
import os


class DemoSpider(scrapy.Spider):
    name = "demo"
    allowed_domains = ["zhihu.com"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        dirPath = os.getcwd() + '/test/data/'
        fileName = dirPath + response.url.split('/')[-2] + '.html'
        with open(fileName, 'wb') as f:
            f.write(response.body)
