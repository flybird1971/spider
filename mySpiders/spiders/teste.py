# -*- coding: utf-8 -*-
import scrapy


class TesteSpider(scrapy.Spider):
    name = "teste"
    allowed_domains = ["teste.com"]
    start_urls = (
        'http://www.teste.com/',
    )

    def parse(self, response):
        pass
