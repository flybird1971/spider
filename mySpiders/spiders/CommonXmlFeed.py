# -*- coding: utf-8 -*-
import re
import mySpiders.utils.log as logging
from scrapy.http import Request
from scrapy.spiders import Spider
from mySpiders.items import XmlFeedItem
from mySpiders.utils.http import getCrawlRequest
from config import MAX_START_URLS_NUM


class XmlFeedSpider(Spider):

    name = 'CommonXmlFeedEx'

    itertag = None

    # allowed_domains = ['zhihu.com']

    start_urls = []

    img_pattern = re.compile(r'<\s*?img.*?src\s*?=\s*?[\'"](.*?)[\'"].*?\>', re.M | re.S)
    text_pattern = re.compile(r'<\s*?(.*?)\>|[\s\n]', re.M | re.S)

    def __init__(self, *arg, **argdict):

        self.titleXpath = ''
        self.descriptionXpath = ''
        self.descriptionLenght = 0
        self.linkXpath = ''
        self.imgUrlXpath = ''
        self.imageNum = 1
        self.videoUrlXpath = ''
        self.pubDateXpath = ''
        self.guidXpath = ''
        self.rule_id = ''
        self.is_remove_namespaces = False
        Spider.__init__(self, *arg,**argdict)
        self.currentNode = None

    def initConfig(self,spiderConfig):

        XmlFeedSpider.itertag = spiderConfig.get('itertag', '')
        self.titleXpath = spiderConfig.get('title_node', '')
        self.descriptionXpath = spiderConfig.get('description_node', '')
        self.descriptionLenght = int(spiderConfig.get('description_length', 1))
        if self.descriptionLenght < 1:
            self.descriptionLenght = 1

        self.linkXpath = spiderConfig.get('guid_node', '')
        self.imgUrlXpath = spiderConfig.get('img_node', '')
        self.imageNum = int(spiderConfig.get('img_num', 1))
        if self.imageNum < 1:
            self.imageNum = 1

        self.videoUrlXpath = spiderConfig.get('video_node', '')
        self.pubDateXpath = spiderConfig.get('public_time', '')
        self.guidXpath = spiderConfig.get('guid_node', '')
        # logging.info("--------guid_node---%s---------------" % self.guidXpath)
        self.rule_id = spiderConfig.get('id', '')
        self.is_remove_namespaces = spiderConfig.get('is_remove_namespaces', 0)
        pass

    def start_requests(self):
        requestUrl = []
        for i in xrange(0,MAX_START_URLS_NUM):
            spiderConfig = getCrawlRequest()
            if not spiderConfig:
                break

            requestUrl.append(Request(spiderConfig.get('start_urls', '')[0],
                                   meta={'spiderConfig':spiderConfig},
                                   callback=self.parse_node,
                                   dont_filter=True))
        return requestUrl
    

    def safeParse(self, xpathPattern):
        """safe about extract datas"""
        if not xpathPattern:
            return []

        return self.currentNode.xpath(xpathPattern).extract()


    def parse_node(self, response):
        
        # if md5(response) == response.meta['spiderConfig'].lastMd5
        #     return []
        # else
        #     md5 = md5(response)

        # logging.info("*********meta******%s****************" % response.meta['spiderConfig'])
        self.initConfig(response.meta['spiderConfig'])

        item = XmlFeedItem()
        self.currentNode = response
        item['title'] = [t.encode('utf-8') for t in self.safeParse(self.titleXpath)]

        imageAndDescriptionInfos = self.parseDescriptionAndImages()
        item['img_url'] = imageAndDescriptionInfos['img_url']
        item['description'] = imageAndDescriptionInfos['description']

        item['public_time'] = [p.encode('utf-8') for p in self.safeParse(self.pubDateXpath)]
        item['source_url'] = [g.encode('utf-8') for g in self.safeParse(self.guidXpath)]
        item['rule_id'] = self.rule_id
        yield item

        # update md5 to mysql
        # spiderConfig = getCrawlRequest(md5,id)
        
        spiderConfig = getCrawlRequest()
        if spiderConfig:
            yield Request(spiderConfig.get('start_urls', '')[0],
                                   headers={'Referer': 'http://www.google.com'},
                                   meta={'spiderConfig':spiderConfig},
                                   callback=self.parse_node,
                                   dont_filter=True)

    def parseDescriptionAndImages(self):
        if not self.imgUrlXpath:
            imgUrlList = []
            descriptionlist = []
            txtList = self.safeParse(self.descriptionXpath)
            txtList = [d.encode('utf-8') for d in self.safeParse(self.descriptionXpath)]
            for txt in txtList:
                extendInfo = self.__parseDescriptionAndImg(txt)
                imgUrlList.append(extendInfo['img_url'])
                descriptionlist.append(extendInfo['description'])
        else:
            txtList = [d.encode('utf-8') for d in self.safeParse(self.descriptionXpath)]
            for txt in txtList:
                descriptionInfos = self.__parseDescriptionOnly(txt)
                descriptionlist.append(descriptionInfos)
            imgUrlList = [d.encode('utf-8') for d in self.safeParse(self.imgUrlXpath)]

        return {"img_url": imgUrlList, "description": descriptionlist}

    def __parseDescriptionOnly(self, text):
        """当img_node存在是，调用此方法获取description"""

        if not text:
            return ""

        txt = self.text_pattern.sub('', text)
        if not txt:
            return text

        if self.descriptionLenght > 0:
            txt = txt.decode('utf8')[0:self.descriptionLenght].encode('utf8')

        return txt

    def __parseDescriptionAndImg(self, text):
        """当img_node不存在是，调用此方法获取description 和 img_url数据"""

        extendItem = {'img_url': '', 'description': ''}
        if not text:
            return extendItem

        imgUrls = self.img_pattern.findall(text)
        if imgUrls:
            extendItem['img_url'] = imgUrls[0:self.imageNum]

        txt = self.text_pattern.sub('', text)
        if not txt:
            txt = text

        if self.descriptionLenght > 0:
            extendItem['description'] = txt.decode('utf8')[0:self.descriptionLenght].encode('utf8')
        return extendItem
