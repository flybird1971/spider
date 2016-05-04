#!/usr/bin/env python
# coding:utf8

import time
from config import MAIN_LOOP_SLEEP_TIME, RUN_SYNC_INTERVAL_TIME

from mySpiders.sql.syncCrawlInfos import SyncCrawlInfos
import mySpiders.utils.log as logging

import sys
reload(sys)
sys.setdefaultencoding("utf8")


class syncDagrame(object):

    def __init__(self):

        self.beginTime = int(time.time())

    def run(self):

        while True:

            self.syncDagrame()
            logging.info("---------------sleep %s senconds " % MAIN_LOOP_SLEEP_TIME)
            time.sleep(MAIN_LOOP_SLEEP_TIME)

    def syncDagrame(self):
        """同步数据到线上"""

        if int(time.time()) - self.beginTime > RUN_SYNC_INTERVAL_TIME:
            logging.info("**********sync crawl infos ************")
            sync = SyncCrawlInfos()
            sync.index()
            self.beginTime = int(time.time())


def mainLoop():
    """ 主循环，捕获异常，并重启rss """

    while True:
        try:
            sync = syncDagrame()
            sync.run()
        except Exception, e:
            logging.info("---------------main loop exception : %s " % e)

if __name__ == '__main__':
    mainLoop()
