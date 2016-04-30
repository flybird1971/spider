# -*- coding: utf-8 -*-

import time
import json
import feedparser
import mySpiders.utils.log as logging
from mySpiders.utils.hash import toMd5
from mySpiders.spiders.BaseFeed import BaseFeed
from mySpiders.utils.http import syncLastMd5
from config import OPEN_MD5_CHECK,REQUEST_TIME_OUT
import socket
socket.setdefaulttimeout(REQUEST_TIME_OUT)
# from mySpiders.utils.CollectionHelper import CollectionHelper


class CommonFeedRss(BaseFeed):

    def run(self, config):

        self.initConfig(config)
        d = feedparser.parse(config.get('start_urls', '')[0])

        # md5校验
        last_md5 = toMd5(d.entries)
        logging.info("*********last_md5 : %s   self.last_md5 : %s*****" % (last_md5, self.last_md5))
        if OPEN_MD5_CHECK and self.last_md5 == last_md5:
            return True

        self.parse(d)  # 解析rss
        syncLastMd5({'last_md5': last_md5, 'id': self.rule_id})

    def parse(self, data):

        RssItemList = {}
        # CollectionHelper.printEx(data)
        for i in data.entries:
            RssItem = {}
            RssItem['source_url'] = i.get('link', '')
            if not RssItem['source_url']:
                continue

            RssItem['unique_code'] = toMd5(RssItem['source_url'])
            RssItem['rule_id'] = self.rule_id
            RssItem['title'] = i.get('title', '')

            text = self.parse_content(i)
            tmpInfos = self.parseContentAndImg(text)
            RssItem['content'] = tmpInfos['content']
            RssItem['img_url'] = json.dumps(tmpInfos['img_url']) if tmpInfos['img_url'] else ""

            RssItem['description'] = self.parseDescription(i)
            RssItem['public_time'] = self.parse_public_time(i)
            RssItem['create_time'] = int(time.time())
            RssItemList[RssItem['unique_code']] = RssItem
            # print RssItem
        self.pipeline.process_item(RssItemList)

    def parse_content(self, data):
        """解析content，兼容处理"""

        text = data.get('content', None)
        if text:
            if isinstance(text, list):
                text = text[0]['value']
            else:
                text = text
            return text

        text = data.get('description', None)
        if text:
            if isinstance(text, list):
                text = text[0]['value']
            else:
                text = text
            return text

        text = data.get('summary', None)
        if text:
            if isinstance(text, list):
                text = text[0]['value']
            else:
                text = text
            return text

        text = ""
        return text

    def parse_public_time(self, data):
        """解析发布时间，兼容处理"""

        public_time = data.get('published_parsed', data.get('updated_parsed', ''))
        if public_time:
            public_time = time.mktime(time.struct_time(public_time))
        else:
            public_time = int(time.time())

        return public_time
