#!/usr/bin/env python
# coding:utf8

import os
import time
import mySpiders.utils.log as logging
from config import MAIN_LOOP_SLEEP_TIME, RUN_SYNC_INTERVAL_TIMES, RUN_SYNC_INTERVAL_TIME
from mySpiders.utils.http import getCrawlNoRssRequestLength
from mySpiders.sql.syncCrawlInfos import SyncCrawlInfos


def startScript():
    times = 0
    beginTime = int(time.time())
    while True:
        try:
            times += 1
            num = getCrawlNoRssRequestLength()
            logging.info("**********need deal request num :%s************" % num)

            if not num:
                logging.info("**********sleep:%s************" % MAIN_LOOP_SLEEP_TIME)
                time.sleep(MAIN_LOOP_SLEEP_TIME)
            else:
                os.system('python runSpider.py')

            if times > RUN_SYNC_INTERVAL_TIMES or int(time.time()) - beginTime > RUN_SYNC_INTERVAL_TIME:
                logging.info("**********sync crawl infos ************")
                sync = SyncCrawlInfos()
                sync.index()
                times = 0
                beginTime = int(time.time())

        except Exception, e:
            logging.info("--------------%------------" % e)


if __name__ == '__main__':
    startScript()
