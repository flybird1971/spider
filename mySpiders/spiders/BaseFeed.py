# -*- coding: utf-8 -*-

import re
import sys
reload(sys)
sys.setdefaultencoding("utf8")

# import os
# sys.path.insert(1,os.path.realpath('../..'))

import mySpiders.utils.log as logging
from mySpiders.pipelines import RssPipeline


class BaseFeed(object):

    img_pattern = re.compile(r'<\s*?img.*?src\s*?=\s*?[\'"](.*?)[\'"].*?\>', re.M | re.S)
    text_pattern = re.compile(r'<\s*?(.*?)\>|[\s\n]', re.M | re.S)

    def __init__(self, *arg, **argdict):
        """ 初始化对象属性 """
        self.pipeline = RssPipeline()

        self.rule = ''
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
        self.checkTxtXpath = ''
        self.is_remove_namespaces = False
        self.last_md5 = ''
        self.next_request_url = ''

    def initConfig(self, spiderConfig):
        """initing"""

        self.rule = spiderConfig.get('rule', '')
        self.titleXpath = spiderConfig.get('title_node', '')
        self.descriptionXpath = spiderConfig.get('description_node', '')
        self.descriptionLenght = int(spiderConfig.get('description_length', 0))
        if self.descriptionLenght < 1:
            self.descriptionLenght = 0

        self.linkXpath = spiderConfig.get('guid_node', '')
        self.imgUrlXpath = spiderConfig.get('img_node', '')
        self.imageNum = int(spiderConfig.get('img_num', 0))
        if self.imageNum < 1:
            self.imageNum = 1

        self.videoUrlXpath = spiderConfig.get('video_node', '')
        self.pubDateXpath = spiderConfig.get('public_time', '')
        self.guidXpath = spiderConfig.get('guid_node', '')

        self.rule_id = spiderConfig.get('id', '')
        self.is_remove_namespaces = spiderConfig.get('is_remove_namespaces', 0)
        self.checkTxtXpath = spiderConfig.get('check_area_node', '//body')
        self.last_md5 = spiderConfig.get('last_md5', '')
        self.next_request_url = spiderConfig.get('next_request_url', '')

    def parseContentAndImg(self, text):
        """当img_node不存在是，调用此方法获取description 和 img_url数据"""

        extendItem = {'img_url': '', 'content': ''}
        if not text:
            return extendItem

        imgUrls = self.img_pattern.findall(text)
        if imgUrls:
            extendItem['img_url'] = imgUrls[0:self.imageNum]

        if self.descriptionLenght > 0:
            extendItem['content'] = text.decode('utf8')[0:self.descriptionLenght].encode('utf8')
        else:
            extendItem['content'] = text

        return extendItem

    def parseDescription(self, data):
        """当img_node存在是，调用此方法获取description"""

        description = data.get('description', data.get('summary', ''))

        if not description:
            return ""

        txt = self.text_pattern.sub('', description)
        if not txt:
            return description

        txt = txt.decode('utf8')[0:1000].encode('utf8')

        return txt
