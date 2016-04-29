# -*- coding: utf-8 -*-
# import re

from scrapy.http import Request
from mySpiders.spiders.MyBaseSpider import MyBaseSpider
import mySpiders.utils.log as logging
from mySpiders.items import CrawlItem

from mySpiders.utils.http import getCrawlNoRssRequest, syncLastMd5
from mySpiders.utils.hash import toMd5
from config import REFERER,OPEN_MD5_CHECK


class CrawlSpider(MyBaseSpider):

    name = 'CrawlSpider'

    start_urls = []

    custom_settings = {
        'ITEM_PIPELINES': {
            'mySpiders.pipelines.CrawlPipeline': 1
        }
    }

    def start_requests(self):

        spiderConfig = getCrawlNoRssRequest()
        if not spiderConfig:
            return []

        self.initConfig(spiderConfig)
        logging.info("*********meta******%s****************" % spiderConfig)
        return [Request(spiderConfig.get('start_urls', '')[0], callback=self.parse, dont_filter=True)]

    def parse(self, response):
        """ 列表页解析 """

        last_md5 = ''
        if self.isFirstListPage:
            checkText = self.safeParse(response, self.checkTxtXpath)
            last_md5 = toMd5(checkText)

        logging.info("*********last_md5 : %s   self.last_md5 : %s*****" % (last_md5, self.last_md5))
        if (not self.is_duplicate) and OPEN_MD5_CHECK and self.isFirstListPage and last_md5 == self.last_md5:
            yield []
        else:
            for request in self.getDetailPageUrls(response):
                yield request

            # 获取下一列表页url
            if not self.isDone:
                for request in self.getNextListPageUrl(response):
                    yield request

            # 同步md5码 & 同步last_id
            if self.isFirstListPage:
                syncLastMd5({'last_md5': last_md5, 'id': self.rule_id})

        self.isFirstListPage = False

    def parse_detail_page(self, response):

        logging.info('--------------------parse detail page-----------')
        item = CrawlItem()
        item['title'] = self.safeParse(response, self.titleXpath)

        imageAndContentInfos = self.parseContentAndImages(response)
        item['img_url'] = imageAndContentInfos['img_url']
        item['content'] = imageAndContentInfos['content']
        item['description'] = self.parseDescription(imageAndContentInfos['content'])

        item['source_score'] = self.parse_score(response)

        item['public_time'] = self.safeParse(response, self.pubDateXpath)
        item['source_url'] = response.url
        item['rule_id'] = self.rule_id
        yield item

    def parse_score(self,response):

        zhuanfa = self.parseNum(self.safeParse(response, self.zhunfaRemarkXpath)) if self.zhunfaRemarkXpath else 0
        bad_remark = self.parseNum( self.safeParse(response, self.badRemarkXpath)) if self.badRemarkXpath else 0
        good_remark = self.parseNum( self.safeParse(response, self.goodRemarkXpath)) if self.goodRemarkXpath else 0
        source_score = int(good_remark) - int(bad_remark) + int(zhuanfa)*20
        return source_score