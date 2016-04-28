#!/usr/bin/env python
# coding:utf8

import time
import gevent
import gevent.monkey
from gevent.pool import Pool
from config import MAIN_LOOP_SLEEP_TIME, RSS_MAX_POOL_NUM, RUN_SYNC_INTERVAL_TIMES, RUN_SYNC_INTERVAL_TIME

from mySpiders.sql.syncCrawlInfos import SyncCrawlInfos
from mySpiders.spiders.CommonFeedRss import CommonFeedRss
from mySpiders.utils.http import getCrawlRequest
import mySpiders.utils.log as logging

import sys
reload(sys)
sys.setdefaultencoding("utf8")

gevent.monkey.patch_socket()


class RssPool(object):

    def __init__(self):

        self.pool = Pool(RSS_MAX_POOL_NUM)
        # self.spider = CommonFeedRss()
        self.start = False
        self.times = 0
        self.beginTime = int(time.time())

    def run(self):

        while True:

            if (not self.start) and (not self.pool.full()):
                self.addRssSpider()
                self.syncDagrame()
                continue

            self.start = False
            if self.pool.free_count() < RSS_MAX_POOL_NUM:
                logging.info("---------------join run ")
                self.pool.join()
            else:
                logging.info("---------------not data ,sleep %s senconds " % MAIN_LOOP_SLEEP_TIME)
                time.sleep(MAIN_LOOP_SLEEP_TIME)

    def syncDagrame(self):
        """同步数据到线上"""
        self.times += 1
        if self.times > RUN_SYNC_INTERVAL_TIMES or int(time.time()) - self.beginTime > RUN_SYNC_INTERVAL_TIME:
            logging.info("**********sync crawl infos ************")
            sync = SyncCrawlInfos()
            sync.index()
            self.times = 0
            self.beginTime = int(time.time())

    def addRssSpider(self):

        configList = getCrawlRequest()
        if not configList:
            self.start = True
            return True

        try:
            spider = CommonFeedRss()
            self.pool.spawn(spider.run, configList)
        except Exception, e:
            logging.info("------------------add spider exception : %s " % e)


def mainLoop():
    """ 主循环，捕获异常，并重启rss """

    while True:
        try:
            rss = RssPool()
            rss.run()
        except Exception, e:
            logging.info("---------------main loop exception : %s " % e)

if __name__ == '__main__':
    mainLoop()
