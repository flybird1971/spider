# -*- coding: utf-8 -*-

import mySpiders.utils.log as logging
from mySpiders.utils.http import syncCrawlInfos
from mySpiders.sql.mysql import Mysql
from config import db_host, db_user, db_password, db_name, db_table_name,SYNC_RECORDS_NUMS
from mySpiders.utils.CollectionHelper import CollectionHelper
import  time

class SyncCrawlInfos(object):

    def __init__(self):

        config = {'host': db_host, 'user': db_user, 'passwd': db_password}
        database = db_name
        self.db = Mysql(config, database)
        self.tableName = db_table_name

    def getRecords(self):

        sql = "select * from " + self.tableName + " where is_sync=0 and sync_times<2 order by id asc limit  " + str(SYNC_RECORDS_NUMS)
        records = self.db.findAll(sql)
        if not records:
            return []

        return list(records)

    def index(self):

        beginTime = int(time.time())
        records = self.getRecords()
        if not records:
            logging.info('no data need sync!!')
            return False

        syncOverData = syncCrawlInfos(records)

        for record in records:
            uniqueCode = record['unique_code']
            if uniqueCode in syncOverData:
                print "sync success %s " % uniqueCode
                updateSql = "update "+self.tableName+" set `is_sync` = 1,`sync_times` = `sync_times`+1 where `unique_code` = '"+uniqueCode+"' "
            else:
                print "sync fail %s " % uniqueCode
                updateSql = "update "+self.tableName+" set `sync_times` = `sync_times`+1 where `unique_code` = '"+uniqueCode+"' "
            self.db.updateBySql(updateSql)


        logging.info('--------------sync records cast time : %s ' % (int(time.time()) - beginTime)  )
        logging.info('--------------sync records success num : %s' % len(syncOverData))
        logging.info('--------------sync records success : %s' % syncOverData )
        logging.info('--------------sync records fail num : %s' % (len(records) - len(syncOverData)))
        return True
