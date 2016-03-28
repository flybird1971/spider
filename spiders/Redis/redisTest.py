#!/usr/bin/env python
#coding:utf-8
import redis

host = '127.0.0.1'
port = 6379
rClient = redis.StrictRedis(host, port)
# rClient.set('liuxuegang','xuagangliu')
# rClient.set('misu',123)


print rClient.get('misu')
print rClient.get('liuxuegang')
print rClient.delete('liuxuegang')