#!/usr/bin/env python
# coding:utf-8

import time
import MySQLdb


class SQL(object):

    def __init__(self):
        self.select = ''
        self.from = ''
        self.groupBy = ''
        self.having = ''
        self.where = ''
        self.join = ''
        self.joinWith = ''
        self.limit = ''
        self.offset = ''
        self.orderBy = ''
        self.sql = ''
        pass

    def addGroupBy(self):
        pass

    def addOrderBy(self):
        pass

    def addSelect(self):
        pass

    def addWhere(self):
        pass

    def addHaving(self):
        pass

    def addOnCondition(self):
        pass

    def count(self):
        pass

    def exists(self):
        pass

    def from(self):
        pass

    def groupBy(self):
        pass

    def having(self):
        pass

    def innerJoin(self):
        pass

    def join(self):
        pass

    def joinWith(self):
        pass

    def leftJoin(self):
        pass

    def limit(self):
        pass

    def max(self):
        pass

    def min(self):
        pass

    def offset(self):
        pass

    def one(self):
        pass

    def orWhere(self):
        pass

    def orderBy(self):
        pass

    def select(self):
        pass

    def where(self):
        pass

    def createCommand(self, sql):
        return self
