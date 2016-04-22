# -*- coding: utf-8 -*-

import mySpiders.utils.log as logging
from mySpiders.utils.http import syncCrawlInfos
from mySpiders.sql.mysql import Mysql
from config import db_host, db_user, db_password, db_name, db_table_name,SYNC_RECORDS_NUMS


class SyncCrawlInfos(object):

    def __init__(self):

        config = {'host': db_host, 'user': db_user, 'passwd': db_password}
        database = db_name
        self.db = Mysql(config, database)
        self.tableName = db_table_name

    def getRecords(self):

        sql = "select * from " + self.tableName + " where is_sync=0 order by id asc limit  " + str(SYNC_RECORDS_NUMS)
        records = self.db.findAll(sql)
        if not records:
            return []

        return list(records)

    def index(self):

        records = self.getRecords()
        if not records:
            logging.info('no data need sync!!')
            return False

        syncOverData = syncCrawlInfos(records)
        for uniqueCode in syncOverData:
            self.db.update(self.tableName, {'is_sync': '1'}, "unique_code = '" + uniqueCode + "'")
        logging.info('--------------sync records success num : %s' % len(syncOverData))
        logging.info('--------------sync records fail num : %s' % (len(records) - len(syncOverData)))
        return True
