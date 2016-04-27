#!/usr/bin/env python
# encoding:utf8

import re
"""
this is collection helper
author : flybird1971@gmail.com
since  : 2015-12-17 11:45:21
"""


class CollectionHelper(object):

    """
    集合序列打印助手
    """

    prefix = "    "
    __MAX_DEEPTH = 0

    def __init__(self): pass

    @staticmethod
    def formatPrint(*data):
        """
        format string
        other function TODO...
        """
        for tmpData in data:
            if not isinstance(tmpData, (str, unicode)):
                print tmpData,
            else:
                regex = re.compile(r'\s', re.M)
                newStr, number = regex.subn(' ', tmpData)
                print newStr,
        print

    @staticmethod
    def printEx(collection, maxDeepth=-1, currentDeepth=0):
        """
        print collection
        """
        CollectionHelper.setMaxDeepth(currentDeepth)
        if isinstance(collection, list):
            CollectionHelper.printList(collection, maxDeepth, currentDeepth)
        elif isinstance(collection, tuple):
            CollectionHelper.printTuple(collection, maxDeepth, currentDeepth)
        elif isinstance(collection, dict):
            CollectionHelper.printDict(collection, maxDeepth, currentDeepth)
        else:
            print CollectionHelper.prefix * currentDeepth, collection

    @staticmethod
    def printList(li, maxDeepth=-1, currentDeepth=0):
        """
        print list collection
        eg : CollectionHelper.printList(list, deepth, maxDeepth)
                 list   将要被打印的列表
                 maxDeepth 最大遍历深度 maxDeepth==-1 表示无限遍历
                 currentDeepth 当前遍历深度
        """
        if maxDeepth != 0 and isinstance(li, list):
            index = 1
            for tmpCollection in li:
                if(isinstance(tmpCollection, (list, tuple, dict))):
                    CollectionHelper.formatPrint(CollectionHelper.prefix*currentDeepth, "list index ", index, ":")
                    CollectionHelper.printEx(
                        tmpCollection, maxDeepth - 1, currentDeepth + 1)
                else:
                    CollectionHelper.formatPrint(CollectionHelper.prefix * currentDeepth, "list index ", index, ":", tmpCollection)
                index += 1
        else:
            CollectionHelper.formatPrint(
                CollectionHelper.prefix * currentDeepth, li)
        pass

    @staticmethod
    def printTuple(tp, maxDeepth=-1, currentDeepth=0):
        """
        print tuple collection
        eg : CollectionHelper.printTuple(lp,maxDeepth,currentDeepth)
                 tuple   将要被打印的元祖
                 maxDeepth 最大遍历深度 maxDeepth==-1 表示无限遍历
                 currentDeepth 当前遍历深度
        """
        if maxDeepth != 0 and isinstance(tp, tuple):
            index = 1
            for tmpCollection in tp:
                if(isinstance(tmpCollection, (list, tuple, dict))):
                    CollectionHelper.formatPrint(CollectionHelper.prefix*currentDeepth, "tuple index ", index, ":")
                    CollectionHelper.printEx(
                        tmpCollection, maxDeepth - 1, currentDeepth + 1)
                else:
                    CollectionHelper.formatPrint(
                        CollectionHelper.prefix * currentDeepth, "tuple index ", index, ":", tmpCollection)
                index += 1
        else:
            CollectionHelper.formatPrint(
                CollectionHelper.prefix * currentDeepth, tp)
        pass

    @staticmethod
    def printDict(diction, maxDeepth=-1, currentDeepth=0):
        """
        print dict collection
        eg : CollectionHelper.printList(dict, maxDeepth, currentDeepth)
                 dict   将要被打印的字典
                 maxDeepth 最大遍历深度 maxDeepth==-1 表示无限遍历
                 currentDeepth 当前遍历深度
        """
        if maxDeepth != 0 and isinstance(diction, dict):
            for tmpCollection in diction:
                if(isinstance(diction[tmpCollection], (list, tuple, dict))) and diction[tmpCollection]:
                    CollectionHelper.formatPrint(
                        CollectionHelper.prefix * currentDeepth, tmpCollection, ":")
                    CollectionHelper.printEx(
                        diction[tmpCollection], maxDeepth - 1, currentDeepth + 1)
                else:
                    CollectionHelper.formatPrint(
                        CollectionHelper.prefix * currentDeepth, tmpCollection, ":", diction[tmpCollection])
        else:
            CollectionHelper.formatPrint(
                CollectionHelper.prefix * currentDeepth, diction)
        pass

    @staticmethod
    def getMaxDeepth():
        return CollectionHelper.__MAX_DEEPTH

    @staticmethod
    def setMaxDeepth(deepth):
        CollectionHelper.__MAX_DEEPTH = deepth if CollectionHelper.__MAX_DEEPTH < deepth else CollectionHelper.__MAX_DEEPTH

if __name__ == "__main__":
    li1 = [(i, i * 2, (i + 1) * 2) for i in xrange(0, 15, 5)]
    li2 = [(i, i * 2, (i + 1) * 2) for i in xrange(0, 21, 5)]
    li3 = [(i, i * 2, (i + 1) * 2) for i in xrange(0, 10, 5)]
    CollectionHelper.printEx((li1, li2, li3))
    print CollectionHelper.getMaxDeepth()