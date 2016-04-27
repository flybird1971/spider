#!/usr/bin/env python
# encoding:utf8

"""
iterable data type to string
demo : 
   dict => str
   list => str
   dict [list] => str
   .......
"""


class Iterable2String(object):

    @staticmethod
    def convert(collection):

        if isinstance(collection, list):
            return Iterable2String.dealList(collection)
        elif isinstance(collection, tuple):
            return Iterable2String.dealTuple(collection)
        elif isinstance(collection, dict):
            return Iterable2String.dealDict(collection)
        else:
            return str(collection)

    @staticmethod
    def dealList(li):

        string = ""
        if isinstance(li, list):
            for tmpCollection in li:
                string += Iterable2String.convert(tmpCollection)
        return string

    @staticmethod
    def dealTuple(tp):

        string = ""
        if isinstance(tp, tuple):
            for tmpCollection in tp:
                string += Iterable2String.convert(tmpCollection)
        return string
        pass

    @staticmethod
    def dealDict(diction):

        string = ""
        if isinstance(diction, dict):
            for tmpCollection in diction:
                string += Iterable2String.convert(diction[tmpCollection])
        
        return string

if __name__ == "__main__":
    li1 = [(i, i * 2, (i + 1) * 2) for i in xrange(0, 15, 5)]
    li2 = [(i, i * 2, (i + 1) * 2) for i in xrange(0, 21, 5)]
    li3 = [(i, i * 2, (i + 1) * 2) for i in xrange(0, 10, 5)]
    print Iterable2String.convert((li1, li2, li3))