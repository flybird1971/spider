#!/usr/bin/env python
#coding:utf-8

import json
import logging
from httpRequest import HttpRequest
# from hash import toMd5

"""
检测 url 是否已经存在
"""
def requstDistinct(hashCode):
    try:
        http = HttpRequest()
        url = 'http://www.babel.com/api/cluster-requst-distinct/index'
        body = {'field':hashCode}
        encryptFields = ['field']
        response = http.setUrl(url).setBody(body).encrypt(encryptFields).post()
        res = json.loads(response)['data']
        if res == '1':
            res = True
        else:
            res = False
    except Exception, e:
        res = None
        logging.info('-----------%s-------' % e)
    finally:
        return res
    
__all__ = ['requstDistinct']

# print requstDistinct(toMd5('http://www.ftchinese.com/story/001066870'))
