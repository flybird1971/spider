#!/usr/bin/env python
#coding:utf-8

from scrapy.spiders import XMLFeedSpider
# from spiders.items import XmlFeedItem
import re

class MyBaseSpider(object):
    """docstring for MyBaseSpider"""
    def __init__(self, arg):
        super(MyBaseSpider, self).__init__()
        self.arg = arg
        


class MyBaseSpider(XMLFeedSpider):
    
    name = 'testxmlfeed'

    # allowed_domains = ['zhihu.com']

    start_urls = []
    iterator = 'iternodes'  # you can change this; see the docs
    itertag = 'channel'  # change it accordingly
    titleXpath = ''
    descriptionXpath = ''
    linkXpath  = ''
    imgUrlXpath = ''
    videoUrlXpath = ''
    pubDateXpath = ''
    guidXpath = ''

    img_pattern = re.compile(r'<\s*?img.*?src\s*?=\s*?[\'"](.*?)[\'"](.*?)\>',re.M|re.S)
    text_pattern = re.compile(r'<\s*?(.*?)\>|[\s\n]',re.M|re.S)

    def __init__(self,*arg,**argdict):
        self.initConfig(*arg,**argdict)
        XMLFeedSpider.__init__(*arg,**argdict)

    def initConfig(self,*arg,**argdict):
        XmlFeedSpider.start_urls = argdict['start_urls']
        XmlFeedSpider.itertag = argdict['itertag']
        XmlFeedSpider.titleXpath = argdict['titleXpath']
        XmlFeedSpider.descriptionXpath = argdict['descriptionXpath']
        XmlFeedSpider.linkXpath = argdict['linkXpath']
        XmlFeedSpider.imgUrlXpath = argdict['imgUrlXpath']
        XmlFeedSpider.videoUrlXpath = argdict['videoUrlXpath']
        XmlFeedSpider.pubDateXpath = argdict['pubDateXpath']
        XmlFeedSpider.guidXpath = argdict['guidXpath']
        pass

    def parse_node(self, response, node):

        item = XmlFeedItem()
        item['title'] = [ t.encode('utf-8') for t in node.xpath(self.titleXpath).extract() ]
        item['link'] =  [ l.encode('utf-8') for l in node.xpath(self.linkXpath).extract() ]
        
        item['img_url'] = []
        item['description'] = []

        txtList = [ d.encode('utf-8') for d in node.xpath(self.descriptionXpath).extract() ]
        for txt in txtList:
            extendInfo = self.parse_description(txt)
            item['img_url'].append(extendInfo['img_url'])
            item['description'].append(extendInfo['description'])

        item['pubDate'] = [ p.encode('utf-8') for p in node.xpath(self.pubDateXpath).extract() ]
        item['guid'] = [ g.encode('utf-8') for g in node.xpath(self.guidXpath).extract() ]
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