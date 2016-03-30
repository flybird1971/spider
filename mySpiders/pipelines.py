# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import time
import logging
from mySpiders.utils.hash import toMd5
from mySpiders.sql.mysql import Mysql


class SpidersPipeline(object):
    def process_item(self, item, spider):
        return item


class CSDNPipeline(object):

    def __init__(self):
        self.file = codecs.open('res.json', mode='a+', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.decode('unicode_escape'))

        return item


class BsbdjPipeline(object):

    def __init__(self):
        self.file = codecs.open('bsbdj_res.json', mode='a+', encoding="utf-8")

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.decode('unicode_escape'))


class XmlFeedPipeline(object):

    # db = None
    # tableName = 'bb_crawl_infos'
    fileOpen = None

    def __init__(self):
        # if not self.db:
        config = {'host':'127.0.0.1','user':'root','passwd':'123456'}
        database = 'babel'
        self.db =  Mysql(config,database)
        self.tableName = 'bb_crawl_infos'
        # return XmlFeedPipeline.db
        # XmlFeedPipeline.connectDB()
        # if not XmlFeedPipeline.fileOpen:
        #     XmlFeedPipeline.fileOpen = codecs.open('xml_feed_zhihu_3.json', mode='a+', encoding="utf-8")
    
    
    # @staticmethod
    # def connectDB():
    #     if XmlFeedPipeline.db == None:
    #         config = {'host':'127.0.0.1','user':'root','passwd':'123456'}
    #         database = 'babel'
    #         XmlFeedPipeline.db =  Mysql(config,database)
    #     return XmlFeedPipeline.db

    def process_item(self, item, spider):
        # line = json.dumps(dict(item)) + "\n"
        # XmlFeedPipeline.fileOpen.write(line)

        rule_id = item['rule_id']
        public_time = int(time.time())
        create_time = int(time.time())
        for index,title in enumerate(item['title']):
            logging.info("-----------%s----------" % item['source_url'][index])
            
            if not item['img_url'][index]:
                img_url = json.dumps(item['img_url'][index])
            else:
                img_url = ''
            
            title = title.decode('utf8')[0:255].encode('utf8')

            insertData = {
                'source_url'  : item['source_url'][index],
                'unique_code' : toMd5(item['source_url'][index]),
                'rule_id'     : rule_id,                
                'title'       : title,      
                'description' : item['description'][index],
                'img_url'     : img_url,
                'public_time' : public_time,
                'create_time' : create_time
            }
            with open('log.insert.sql','a+') as f:
                infos = json.dumps(dict(insertData))
                # logging.info("-----------%s----------------" % infos)
                f.write(infos)
            self.db.insert(self.tableName,insertData)
        
        return True