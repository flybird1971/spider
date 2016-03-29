# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider
from mySpiders.items import XmlFeedItem
import re

class TestxmlfeedSpider(XMLFeedSpider):
    
    name = 'testxmlfeed'

    # allowed_domains = ['zhihu.com']

    start_urls = [
        'http://zhihurss.miantiao.me/zhihuzhuanlan/taosay?limit=20'
    ]

    iterator = 'iternodes'  # you can change this; see the docs
    
    itertag = 'channel'  # change it accordingly

    img_pattern = re.compile(r'<\s*?img.*?src\s*?=\s*?[\'"](.*?)[\'"](.*?)\>',re.M|re.S)

    text_pattern = re.compile(r'<\s*?(.*?)\>|[\s\n]',re.M|re.S)

    def parse_node(self, response, node):

        item = XmlFeedItem()
        item['title'] = [ t.encode('utf-8') for t in node.xpath('item/title/text()').extract() ]
        item['link'] =  [ l.encode('utf-8') for l in node.xpath('item/link/text()').extract() ]
        
        item['img_url'] = []
        item['description'] = []

        txtList = [ d.encode('utf-8') for d in node.xpath('item/description/text()').extract() ]
        for txt in txtList:
            extendInfo = self.parse_description(txt)
            item['img_url'].append(extendInfo['img_url'])
            item['description'].append(extendInfo['description'])

        item['pubDate'] = [ p.encode('utf-8') for p in node.xpath('item/pubDate/text()').extract() ]
        item['guid'] = [ g.encode('utf-8') for g in node.xpath('item/guid/text()').extract() ]
        yield item


    def parse_description(self,text):

        extendItem = {'img_url':'','description':''}
        if not text: return extendItem

        imgUrls = self.img_pattern.search(text)
        if imgUrls :
            extendItem['img_url'] = imgUrls.group(1)

        txt = self.text_pattern.sub('',text)
        if not txt:
            txt = text

        extendItem['description'] = txt.decode('utf8')[0:50].encode('utf8')

        return extendItem