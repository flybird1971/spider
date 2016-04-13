#!/usr/bin/env python
# coding:utf-8

import md5
import base64


def toMd5(data):

    if isinstance(data, (list, dict, tuple, set)):
        string = " ".join(data)
    else:
        string = data
    string = string.encode('utf-8')
    m = md5.new()
    m.update(string)
    return m.hexdigest()


def base64Encode(data):
    return base64.b64encode(data)


def base64Decode(data):
    return base64.b64decode(data)

__all__ = ['toMd5']
