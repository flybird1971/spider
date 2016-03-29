#!/usr/bin/env python
# coding:utf8

import json
from mySpiders.utils.httpRequest import HttpRequest


def getCrawlRequest():
    try:
        http = HttpRequest()
        url = 'http://www.babel.com/api/get-spider-rules/get'
        body = {'action': 'get', 'version': '1.1'}
        encryptFields = ['action', 'version']
        res = http.setUrl(url).setBody(body).encrypt(encryptFields).post()
        res = json.loads(res)['data']
        if res == 'null':
            res = None
    except Exception, e:
        print e
        return None
    finally:
        pass
    return res

if __name__ == '__main__':
    print getCrawlRequest()
