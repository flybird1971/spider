#!/usr/bin/env python
# coding:utf8

import os
import time

while True:
    try:
        print "================================"
        time.sleep(2)
        os.system('python test.py')
    except Exception, e:
        print "--------------%------------" % e
