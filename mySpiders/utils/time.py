#!/usr/bin/env python
#coding:utf-8

import datetime
import time
from dateutil.parser import parse


def getDate():
        return datetime.datetime.now().strftime('%Y-%m-%d')


def strtimetime(timeStr):
    return datetime.datetime.strptime(timeStr.timetuple())
    # return parse('26 May 2009 19:58:20').strftime('%s')
    # return parse(timeStr).strftime('%s')
    
#把datetime转成字符串
def datetime_toString(dt):
    return dt.strftime("%Y-%m-%d-%H")

#把字符串转成datetime
def string_toDatetime(string):
    return datetime.strptime(string, "%Y-%m-%d-%H")

#把字符串转成时间戳形式
def string_toTimestamp(strTime):
    return time.mktime(string_toDatetime(strTime).timetuple())

#把时间戳转成字符串形式
def timestamp_toString(stamp):
    return time.strftime("%Y-%m-%d-%H", tiem.localtime(stamp))

#把datetime类型转外时间戳形式
def datetime_toTimestamp(dateTim):
    return time.mktime(dateTim.timetuple())

print  strtimetime('Wed, 30 Mar 2016 07:05:47')