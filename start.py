#!/usr/bin/env python
# coding:utf8

import os
import time
import mySpiders.utils.log as logging
from config import MAIN_LOOP_SLEEP_TIME
from mySpiders.utils.http import getCrawlRequestLength
from mySpiders.sql.syncCrawlInfos import SyncCrawlInfos


def startScript():
    while True:
        try:
            num = getCrawlRequestLength()
            logging.info("**********need deal request num :%s************" % num, True)

            if not num:
                sync = SyncCrawlInfos()
                sync.index()
                logging.info("**********sleep:%s************" % MAIN_LOOP_SLEEP_TIME, True)
                time.sleep(MAIN_LOOP_SLEEP_TIME)
            else:
                os.system('python runSpider.py')
        except Exception, e:
            logging.info("--------------%------------" % e, True)


if __name__ == '__main__':
    startScript()
