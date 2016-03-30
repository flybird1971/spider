#!/usr/bin/env python
#coding:utf-8

import md5

def toMd5(data):
        m = md5.new()
        m.update(data);
        return m.hexdigest()

__all__=['toMd5']