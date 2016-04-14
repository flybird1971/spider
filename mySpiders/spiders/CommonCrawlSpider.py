# -*- coding: utf-8 -*-
import re
import mySpiders.utils.log as logging
from scrapy.http import Request
from scrapy.spiders import Spider
from mySpiders.items import XmlFeedItem
from mySpiders.utils.http import getCrawlRequest, syncLastMd5, requstDistinct
from config import REFERER
from mySpiders.utils.hash import toMd5

"""
概略：

    1. 爬取通用非RSS文本&博客列表页面

    2. 对验证区域进行MD5校验，校验通过执行，否则执行下个spider_rules
        tips：此处校验不通过，直接跳过对这个spider_rules的后续抓取

    3. 分析downloader列表页面内容，获取详情页面urls

    4. 对获取的详情页面urls，进行批量校验是否重复【redis]，去重

    5. push详情页面urls到调度器，并指定有parse_detail_page函数进行解析

    6. 根据【下一页】获取下个列表页面url，并push到调度器，且指定parse_node函数进行解析

    7. 重复第一步

parse_node函数：

    1. 根据spider_rules.next_request_url 获取下个列表页面url
        tips: 容错处理，如果异常数据，直接使用服务端日志上传接口，上传错误信息，
              并终止此次crawl，要求日志上传在配置中进行开启&关闭配置

    2. 成功直接push到调度器

parse_detail_page函数：

    1. 根据spider_rules配置中 title_node，description_node，description_length，image_node，image_length，author_node，
        public_node等节点配置extract详情页面
        tips : 注意此处容错处理，要求失败必须上传失败日志，作为后续分享依据

    2. yield 处理结果
        tips: piplines中不再对url是否重复进行判断

    3. insert into mysqlDB

日志上传要求：

    当前详情页面url, 时间，md5码，
    多次上传同一个url时，后台服务器需要更新记录，而不是重新插入新记录
    上传日志，不需要进行回执确认处理


rules配置及容错处理：

    author_node 不存在，则默认空，否则进行extract
    image_node  不存在，正则取文本内容img_url，否则直接extract
    image_lenght 强制>=0

    description_length 强制>=25

    link_node   不存在，使用response.url填充
    video_node  不存在，则默认空，否则进行extract


"""


class CommonCrawlSpider(Spider):

    name = 'CommonCrawlSpider'

    # allowed_domains = ['zhihu.com']

    start_urls = []

    img_pattern = re.compile(r'<\s*?img.*?src\s*?=\s*?[\'"](.*?)[\'"].*?\>', re.M | re.S)
    text_pattern = re.compile(r'<\s*?(.*?)\>|[\s\n]', re.M | re.S)

    def __init__(self, *arg, **argdict):
        """ 初始化对象属性 """

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
        Spider.__init__(self, *arg, **argdict)
        self.currentNode = None
        self.isDone = False
        self.isFirstListPage = True

    def initConfig(self, spiderConfig):
        """initing"""

        self.rule = spiderConfig.get('rule', '')
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
        self.checkTxtXpath = spiderConfig.get('check_area_node', '//body')

    def start_requests(self):

        spiderConfig = getCrawlRequest()
        if not spiderConfig:
            return []

        self.initConfig(spiderConfig)
        # logging.info("*********meta******%s****************" % response.meta['spiderConfig'])
        yield Request(spiderConfig.get('start_urls', '')[0],
                      callback=self.parse, dont_filter=True)

    def parse(self, response):
        """ 列表页解析 """

        self.isDone = False
        self.currentNode = response

        last_md5 = ''
        if self.isFirstListPage:
            checkText = self.safeParse(self.checkTxtXpath)
            last_md5 = toMd5(checkText)

        if self.isFirstListPage and last_md5 == response.meta['spiderConfig'].get('last_md5', ''):
            yield []
        else:
            self.getDetailPageUrls()

            # 获取下一列表页url
            if not self.isDone:
                self.getNextListPageUrl()

            # 同步md5码 & 同步last_id
            if self.isFirstListPage:
                syncLastMd5({'last_md5': last_md5, 'id': self.rule_id})

        self.isFirstListPage = False

    def getNextListPageUrl(self):

        nextListPageURL = [t.encode('utf-8') for t in self.safeParse(self.next_request_url)]

        if len(nextListPageURL) < 0:
            yield []

        yield Request(nextListPageURL[0], headers={'Referer': REFERER}, callback=self.parse, dont_filter=True)

    def getDetailPageUrls(self):

        detailUrls = [t.encode('utf-8') for t in self.safeParse(self.rule)]
        # 批量验证urls是否重复
        detailUrlsByFilter = self.distinctRequestUrls(detailUrls)
        if len(detailUrls) < 1 or len(detailUrlsByFilter) != len(detailUrls):
            self.isDone = True

        if detailUrlsByFilter:
            requestUrl = []
            for i in detailUrlsByFilter:
                requestUrl.append(Request(detailUrlsByFilter[i], callback=self.parse_detail_page, dont_filter=True))
            yield requestUrl

    def distinctRequestUrls(self, urls):

        if len(urls) < 1:
            return []

        uniqueCodeDict = {}
        for i in urls:
            uniqueCodeDict[toMd5(urls[i])] = urls[i]
        repeatUniqueCode = requstDistinct(uniqueCodeDict.keys())
        for i, unique in enumerate(repeatUniqueCode):
            del(uniqueCodeDict[unique])
        return uniqueCodeDict.values()

    def safeParse(self, xpathPattern):
        """safe about extract datas"""

        if not xpathPattern:
            return []

        return self.currentNode.xpath(xpathPattern).extract()

    def parse_detail_page(self, response):

        self.currentNode = response
        item = XmlFeedItem()
        item['title'] = [t.encode('utf-8') for t in self.safeParse(self.titleXpath)]

        imageAndDescriptionInfos = self.parseDescriptionAndImages()
        item['img_url'] = imageAndDescriptionInfos['img_url']
        item['description'] = imageAndDescriptionInfos['description']

        item['public_time'] = [p.encode('utf-8') for p in self.safeParse(self.pubDateXpath)]
        item['source_url'] = [g.encode('utf-8') for g in self.safeParse(self.guidXpath)]
        item['rule_id'] = self.rule_id
        yield item

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
