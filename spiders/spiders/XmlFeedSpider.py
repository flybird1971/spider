# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider
from spiders.items import XmlFeedItem
import re
import time

class XmlFeedSpider(XMLFeedSpider):
    
    name = 'testxmlfeed'

    # allowed_domains = ['zhihu.com']

    start_urls = []
    iterator = 'iternodes'  # you can change this; see the docs
    itertag = 'channel'  # change it accordingly
    titleXpath = ''
    descriptionXpath = ''
    descriptionLenght = 0
    linkXpath  = ''
    imgUrlXpath = ''
    imageNum = 1
    videoUrlXpath = ''
    pubDateXpath = ''
    guidXpath = ''
    rule_id = ''


    img_pattern = re.compile(r'<\s*?img.*?src\s*?=\s*?[\'"](.*?)[\'"](.*?)\>',re.M|re.S)
    text_pattern = re.compile(r'<\s*?(.*?)\>|[\s\n]',re.M|re.S)

    def __init__(self,*arg,**argdict):
        self.initConfig(*arg,**argdict)
        XMLFeedSpider.__init__(*arg,**argdict)

    def initConfig(self,*arg,**argdict):
        XmlFeedSpider.start_urls = argdict.get('start_urls','')
        XmlFeedSpider.itertag = argdict.get('itertag','')
        XmlFeedSpider.titleXpath = argdict.get('titleXpath','')
        XmlFeedSpider.descriptionXpath = argdict.get('descriptionXpath','')
        XmlFeedSpider.descriptionLenght = argdict.get('descriptionLenght',0)
        XmlFeedSpider.linkXpath = argdict.get('linkXpath','')
        XmlFeedSpider.imgUrlXpath = argdict.get('imgUrlXpath','')
        XmlFeedSpider.imageNum = argdict.get('imageNum',1)
        XmlFeedSpider.videoUrlXpath = argdict.get('videoUrlXpath','')
        XmlFeedSpider.pubDateXpath = argdict.get('pubDateXpath','')
        XmlFeedSpider.guidXpath = argdict.get('guidXpath','')
        XmlFeedSpider.rule_id = argdict.get('rule_id','')
        pass

    def safeParse(self,sel,xpathPattern):
        """safe about extract datas"""
        if not xpathPattern:
            return []

        return sel.xpath(xpathPattern).extract()


    def parse_node(self, response, node):

        item = XmlFeedItem()
        item['title'] = [ t.encode('utf-8') for t in self.safeParse(self.titleXpath) ]
        # item['link'] =  [ l.encode('utf-8') for l in self.safeParse(self.linkXpath) ]
        
        item['img_url'] = []
        item['description'] = []

        txtList = [ d.encode('utf-8') for d in self.safeParse(self.descriptionXpath) ]
        for txt in txtList:
            extendInfo = self.parse_description(txt)
            item['img_url'].append(extendInfo['img_url'])
            item['description'].append(extendInfo['description'])

        item['public_time'] = [ p.encode('utf-8') for p in self.safeParse(self.pubDateXpath) ]
        item['source_url'] = [ g.encode('utf-8') for g in self.safeParse(self.guidXpath) ]
        item['rule_id'] = self.rule_id
        item['create_time'] = time.time()
        yield item


    def parse_description(self,text):

        extendItem = {'img_url':'','description':''}
        if not text: return extendItem

        imgUrls = self.img_pattern.findall(text)
        if imgUrls :
            extendItem['img_url'] = imgUrls.group(1)[0:self.imageNum]

        txt = self.text_pattern.sub('',text)
        if not txt:
            txt = text

        if self.descriptionLenght > 0:
            extendItem['description'] = txt.decode('utf8')[0:self.descriptionLenght].encode('utf8')

        return extendItem