#!/usr/bin/env python
#coding:utf-8
import redis
import json
import logging

# host = '127.0.0.1'
# port = 6379
# rClient = redis.StrictRedis(host, port)

class BaseRedis(object):

    rClient = None

    def __init__(self,host='127.0.0.1',port='6379',db=0,password=None):
        self.host = host
        self.port = port
        self.db = db
        self.password = password

    def connect(self):
        if not ClusterRequstDistinct.rClient: 
            logging.info("--------------redis--connection------------")
            ClusterRequstDistinct.rClient = redis.StrictRedis(self.host, self.port,self.db,self.password)
            # ClusterRequstDistinct.rClient = redis.StrictRedis(self.host, self.port)
            #  __init__(self, host='localhost', port=6379, db=0, password=None, socket_timeout=None, 
            #  socket_connect_timeout=None, socket_keepalive=None, socket_keepalive_options=None, connection_pool=None, 
            #  unix_socket_path=None, encoding='utf-8', encoding_errors='strict', charset=None, errors=None, decode_responses=False, 
            #  retry_on_timeout=False, ssl=False, ssl_keyfile=None, ssl_certfile=None, ssl_cert_reqs=None, ssl_ca_certs=None, max_connections=None)
            # print help(redis.StrictRedis)
        return ClusterRequstDistinct.rClient

    def set(self,key,val,isString=True):
        self.connect()
        if not isString:
            val = json.dumps(val)
        return ClusterRequstDistinct.rClient.set(key,val)

    def get(self,key):
        self.connect()
        return ClusterRequstDistinct.rClient.get(key)

    def delete(self,key):
        self.connect()
        return ClusterRequstDistinct.rClient.delete(key)        


class ClusterRequstDistinct(BaseRedis):

    def hSet(self,key,field,val,isString=True):
        self.connect()
        if not isString:
            val = json.dumps(val)
        return ClusterRequstDistinct.rClient.hset(key,field,val)

    def hGet(self,key,field,isString=True):
        self.connect()
        res = ClusterRequstDistinct.rClient.hget(key,field)
        if not isString:
            res = json.dumps(res)
        return res

    def hDel(self,key,field):
        self.connect()
        return ClusterRequstDistinct.rClient.hdel(key,field)

if __name__ == '__main__':
    # requestRedis = ClusterRequstDistinct(host='127.0.0.1',port='6379',db=0,password=None)
    requestRedis = ClusterRequstDistinct(host='123.57.7.227',port='6379',db=0,password='lx1123581321LX')
    print requestRedis.hSet('unique_request_mySpider','xuegang.liu22',True)
    print "*"*88
    print requestRedis.hDel('unique_request_mySpider','xuegang.liu22')
    print "*"*88
    print requestRedis.hGet('unique_request_mySpider','xuegang.liu22')

    # print rClient.get('misu')
    # print rClient.get('liuxuegang')
    # print rClient.delete('liuxuegang')