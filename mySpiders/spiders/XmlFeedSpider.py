# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider
from mySpiders.items import XmlFeedItem
import re
import time

class XmlFeedSpider(XMLFeedSpider):
    
    name = 'CommonXmlFeed'

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
        self.currentNode = None

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

    def safeParse(self,xpathPattern):
        """safe about extract datas"""
        if not xpathPattern:
            return []

        return self.currentNode.xpath(xpathPattern).extract()


    def parse_node(self, response, node):

        item = XmlFeedItem()
        self.currentNode = node
        item['title'] = [ t.encode('utf-8') for t in self.safeParse(self.titleXpath) ]

        imageAndDescriptionInfos = self.parseDescriptionAndImages()
        item['img_url'] = imageAndDescriptionInfos['img_url']
        item['description'] = imageAndDescriptionInfos['description']

        item['public_time'] = [ p.encode('utf-8') for p in self.safeParse(self.pubDateXpath) ]
        item['source_url'] = [ g.encode('utf-8') for g in self.safeParse(self.guidXpath) ]
        item['rule_id'] = self.rule_id
        item['create_time'] = time.time()
        yield item


    def parseDescriptionAndImages(self):
        if not self.imgUrlXpath:
            imgUrlList = descriptionlist = []
            txtList = [ d.encode('utf-8') for d in self.safeParse(self.descriptionXpath) ]
            for txt in txtList:
                extendInfo = self.__parseDescriptionAndImg(txt)
                imgUrlList.append(extendInfo['img_url'])
                descriptionlist.append(extendInfo['description'])
        else:
            txtList = [ d.encode('utf-8') for d in self.safeParse(self.descriptionXpath) ]
            for txt in txtList:
                descriptionInfos = self.__parseDescriptionOnly(txt)
                descriptionlist.append(descriptionInfos)
            imgUrlList = [ d.encode('utf-8') for d in self.safeParse(self.imgUrlXpath) ]
        
        return {"img_url":imgUrlList,"description":descriptionlist}
        


    def __parseDescriptionOnly(self,text):
        """当img_node存在是，调用此方法获取description"""

        if not text: return ""

        txt = self.text_pattern.sub('',text)
        if not txt: return text

        if self.descriptionLenght > 0:
            txt = txt.decode('utf8')[0:self.descriptionLenght].encode('utf8')

        return txt

    def __parseDescriptionAndImg(self,text):
        """当img_node不存在是，调用此方法获取description 和 img_url数据"""

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