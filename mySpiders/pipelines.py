# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import time
import mySpiders.utils.log as logging
from mySpiders.utils.hash import toMd5
from mySpiders.sql.mysql import Mysql
from mySpiders.utils.http import requstDistinct
from config import db_host, db_user, db_password, db_name, db_table_name,OPEN_REDIS_DISTINCT


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


class ToutiaoPipeline(object):

    def __init__(self):

        config = {'host': db_host, 'user': db_user, 'passwd': db_password}
        database = db_name
        self.db = Mysql(config, database)
        self.tableName = 'bb_toutiao_sources'
        self.item = None

    def process_item(self, item, spider):

        if not item:
            logging.info('-----------------------list page repeat : %s' % item)
            return True

        public_time = int(time.time())
        create_time = int(time.time())

        for i in xrange(0, len(item['url'])):
            insertData = {
                'title': item['title'][i],
                'url': item['url'][i],
                'unique_code': toMd5(item['url'][i]),
                'share_num': item['share_num'][i],
                'rss_num': item['rss_num'][i],
                'public_time': public_time,
                'create_time': create_time
            }
            self.db.insert(self.tableName, insertData)

        return True


class CommonCrawlPipeline(object):

    def __init__(self):

        config = {'host': db_host, 'user': db_user, 'passwd': db_password}
        database = db_name
        self.db = Mysql(config, database)
        self.tableName = db_table_name
        self.item = None

    def process_item(self, item, spider):

        if not item:
            logging.info('--------item is empty : %s' % item)
            return True

        rule_id = item['rule_id']
        public_time = int(time.time())
        create_time = int(time.time())

        img_url = json.dumps(item['img_url'])
        description = item['description']
        if not description:
            return True

        title = item['title'].decode('utf8')[0:255].encode('utf8')
        insertData = {
            'source_url': item['source_url'],
            'unique_code': toMd5(item['source_url']),
            'rule_id': rule_id,
            'title': title,
            'description': description,
            'img_url': img_url,
            'public_time': public_time,
            'create_time': create_time
        }
        self.db.insert(self.tableName, insertData)
        return True


class XmlFeedPipeline(object):

    def __init__(self):

        config = {'host': db_host, 'user': db_user, 'passwd': db_password}
        database = db_name
        self.db = Mysql(config, database)
        self.tableName = db_table_name
        self.item = None

    def process_item(self, item, spider):

        if not item:
            logging.info('-----------------------list page repeat ')
            return True

        self.item = item
        insertDataList = self.filterAndPackageDgrate()
        for index in insertDataList:
            self.db.insert(self.tableName, insertDataList[index])

        return True

    def filterAndPackageDgrate(self):

        uniqueCodeList = []
        insertData = {}
        item = self.item

        rule_id = item['rule_id']
        public_time = int(time.time())
        create_time = int(time.time())

        for index, title in enumerate(item['title']):

            uniqueCode = toMd5(item['source_url'][index])
            if index < len(item['img_url']) and item['img_url'][index]:
                img_url = json.dumps(item['img_url'][index])
            else:
                img_url = ''

            if index < len(item['description']) and item['description'][index]:
                description = item['description'][index]
            else:
                continue

            title = title.decode('utf8')[0:255].encode('utf8')
            uniqueCodeList.append(uniqueCode)
            insertData[uniqueCode] = {
                'source_url': item['source_url'][index],
                'unique_code': uniqueCode,
                'rule_id': rule_id,
                'title': title,
                'description': description,
                'img_url': img_url,
                'public_time': public_time,
                'create_time': create_time
            }

        if uniqueCodeList and OPEN_REDIS_DISTINCT:
            repeatUniqueCode = requstDistinct(uniqueCodeList)
            for i, unique in enumerate(repeatUniqueCode):
                del(insertData[unique])

        return insertData




#  专供rss手动实现爬虫使用
class RssPipeline(object):

    def __init__(self):

        config = {'host': db_host, 'user': db_user, 'passwd': db_password}
        database = db_name
        self.db = Mysql(config, database)
        self.tableName = db_table_name
        self.item = None

    def process_item(self, item):

        if not item:
            logging.info('------------page not crawl data ')
            return True

        self.item = item
        insertDataList = self.filterAndPackageDgrate()
        for index in insertDataList:
            self.db.insert(self.tableName, insertDataList[index])

        return True

    def filterAndPackageDgrate(self):

        if not OPEN_REDIS_DISTINCT:
            return self.item

        uniqueCodeList = self.item.keys()
        repeatUniqueCode = requstDistinct(uniqueCodeList)
        logging.info('------------distinct before : %s ' % uniqueCodeList)
        for i, unique in enumerate(repeatUniqueCode):
            del(self.item[unique])
        logging.info('------------distinct after : %s ' % self.item.keys())
        return self.item


# 专供非rss 爬虫使用
class CrawlPipeline(object):

    def __init__(self):

        config = {'host': db_host, 'user': db_user, 'passwd': db_password}
        database = db_name
        self.db = Mysql(config, database)
        self.tableName = db_table_name
        self.item = None

    def process_item(self, item, spider):

        if not item:
            logging.info('--------item is empty : %s' % item)
            return True

        create_time = int(time.time())
        img_url = json.dumps(item['img_url'])
        if (not item['description']) and (not item['content']):
            return True

        title = item['title'].decode('utf8')[0:255].encode('utf8')
        insertData = {
            'source_url': item['source_url'],
            'unique_code': toMd5(item['source_url']),
            'rule_id': item['rule_id'],
            'title': title,
            'description': item['description'],
            'content': item['content'],
            'img_url': img_url,
            'source_score' : item['source_score'],
            'is_sync' : '0',
            'public_time': item['public_time'],
            'create_time': create_time
        }
        insertOk = self.db.insert(self.tableName, insertData)
        if ( not insertOk )and spider.is_duplicate:
            self.db.update(self.tableName, insertData, "unique_code = '" + insertData['unique_code'] + "'")
            logging.info('========update.unique_code : %s' % insertData['unique_code'])

        return True