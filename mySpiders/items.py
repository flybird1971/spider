# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class BsbdjItem(Item):
    name = Field()
    url = Field()


class MyspidersItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CSDNItem(Item):
    name = Field()
    url = Field()


class DemoItem(Item):
    title = Field()
    href = Field()
    desc = Field()
    pass


class StackOverflowItem(Item):
    title = Field()
    tags = Field()
    body = Field()
    href = Field()
    pass


class XmlFeedItem(Item):
    source_url = Field()
    unique_code = Field()
    rule_id = Field()
    title = Field()
    description = Field()
    img_url = Field()
    video_url = Field()
    public_time = Field()
    create_time = Field()
    pass
