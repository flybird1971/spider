#!/usr/bin/env python
# coding:utf-8

import md5


def toMd5(data):

    if isinstance(data, (list, dict, tuple, set)):
        string = " ".join(data)
    else:
        string = data
    string = string.encode('utf-8')
    m = md5.new()
    m.update(string)
    return m.hexdigest()

__all__ = ['toMd5']
