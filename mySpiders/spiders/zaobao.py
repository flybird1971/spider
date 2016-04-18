# -*- coding: utf-8 -*-
import scrapy


class ZaobaoSpider(scrapy.Spider):
    # 爬虫名称，工程中要求唯一
    name = "zaobaos"

    # 允许的域名
    allowed_domains = ["zaobao.com"]

    # 初始待抓取url列表
    start_urls = (
        'http://www.zaobao.com/',
    )

    # 用户设置，会覆盖全局设置
    custom_settings = (

    )

    # 抓取器，spider将绑定到它上面
    crawler = {}

    # 配置实例，包含工程中所有配置变量
    settings = {}

    # 日志实例
    logger = {}

    def parse(self, response):
        trs = response.xpath('//*[@id="hot-novel"]/div[2]/div[1]/ul/li[3]/a')
        for tr in trs:
            trs.xpath('a/text()').extract()
        pass
