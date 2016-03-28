#!/usr/bin/env python
# coding:utf8

import scrapy


class StackOverflowSpider(scrapy.Spider):

    name = 'stackoverflow'
    start_urls = [
        'http://stackoverflow.com/questions?sort=votes'
    ]

    def parse(self, response):
        for href in response.css('.question-summary h3 a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_question)

    def parse_question(self, response):
        yield {
            'title': response.css('h1 a::text').extract()[0],
            'votes': response.css('.question .vote-count-post::text').extract()[0],
            'body': response.css('.question .post-text').extract()[0][0:12],
            'tags': response.css('.question .post-tag::text').extract()[0],
            'link': response.url,
        }
