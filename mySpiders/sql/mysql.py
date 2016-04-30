# coding:utf8
import MySQLdb as mdb
import mySpiders.utils.log as logging
# import sys
# sys.path.append("../")
__author__ = 'flybird1971'

# 参加文档 http://zetcode.com/db/mysqlpython/


class BaseMysql(object):
    """docstring for BaseMysql"""

    def __init__(self):
        super(BaseMysql, self).__init__()

    def where(self, where):
        pass

    def orderBy(self, where):
        pass

    def limit(self, limit):
        pass

    def offset(self, offset):
        pass

    def groupBy(self, groupBy):
        pass

    def having(self, having):
        pass

    def setTable(self, tableName):
        pass

    def packSql(self):
        pass


class Mysql(BaseMysql):

    def __init__(self, config, database):
        super(Mysql, self).__init__()
        self.host = config.get('host', '127.0.0.1')
        self.user = config.get('user', 'root')
        self.passwd = config.get('passwd', '')
        self.connect = None
        self.cur = None
        self.isDict = True

        if not database:
            raise Exception("database must passed")
        self.database = database

    def __connect(self):
        """connect mysql db"""
        self.connect = mdb.connect(host=self.host, user=self.user, passwd=self.passwd, charset='utf8')  # 建立连接
        self.connect.select_db(self.database)  # 选择数据库

        # 创建游标
        if self.isDict:
            self.cur = self.connect.cursor(mdb.cursors.DictCursor)
        else:
            self.cur = self.connect.cursor()
        self.cur.execute("SET NAMES utf8")

    def setDictCur(self, isDict=True):
        self.isDict = isDict
        pass

    def __initConnect(self):
        if not self.cur or not self.connect:
            self.__connect()
        return True

    def findOne(self, sql, params=None):
        try:
            self.__initConnect()
            if params is None:
                self.cur.execute(sql)
            else:
                self.cur.execute(sql, params)
            res = self.cur.fetchone()
            return res
        except mdb.Error, e:
            print "has error %d : %s " % (e.args[0], e.args[1])
            return None
        finally:
            self.close()
        return None

    def findAll(self, sql, params=None):
        try:
            self.__initConnect()
            if params is None:
                self.cur.execute(sql)
            else:
                self.cur.execute(sql, params)
            rows = self.cur.fetchall()
            return rows
        except mdb.Error, e:
            print "has error %d : %s " % (e.args[0], e.args[1])
            return None
        finally:
            self.close()
        return None

    def toString(self, data):

        res = []
        for i in data:
            res.append(i)
            # res.append(str(i))
        # res = "'" +  "','".join(res).strip(',') + "'"
        return res

    def packPlaceholder(self, num):
        if not num:
            raise Exception('num error to packPlaceholder')

        placeholder = "%s," * num
        placeholder = placeholder.strip(",")
        return placeholder

    def insert(self, tableName, insertData):
        try:
            self.__initConnect()
            with self.connect:
                dataList = self.toString(insertData.values())
                placeholder = self.packPlaceholder(len(insertData.keys()))
                # insertSql = "insert into "+ tableName +" ("+ ",".join(insertData.keys())+") values ( "+data+")"
                insertSql = "insert into " + tableName + \
                    " (" + ",".join(insertData.keys()) + ") values ( " + placeholder + ")"
                self.cur.execute(insertSql, dataList)
                return self.cur.rowcount
            self.connect.commit()  # 事务自动开启提交
        except mdb.Error, e:
            self.connect.rollback()
            print "has error %d : %s " % (e.args[0], e.args[1])
            return None
        finally:
            self.close()
        return None

    def batchInsert(self, tableName, fieldTuple, insertDataList):
        """批量插入数据"""
        try:
            self.__initConnect()
            with self.connect:
                placeholder = self.packPlaceholder(len(fieldTuple))
                insertSql = "insert into " + tableName + " (" + ",".join(fieldTuple) + ") values ( " + placeholder + ")"
                dataList = [self.toString(i) for i in insertDataList]
                self.cur.executemany(insertSql, dataList)
                return self.cur.rowcount
            self.connect.commit()  # 事务自动开启提交
        except mdb.Error, e:
            self.connect.rollback()
            print "has error %d : %s " % (e.args[0], e.args[1])
            return None
        finally:
            self.close()
        return None

    def update(self, tableName, updateDict, where=''):
        """更新数据"""
        try:
            self.__initConnect()
            with self.connect:
                updateSql = "update " + tableName + " set "
                for field in updateDict.keys():
                    updateSql += " `"+ field +"` = %s,"
                updateSql = updateSql.strip(',')

                if not where:
                    where = "1=1"
                updateSql += " where " + where
                self.cur.execute(updateSql, updateDict.values())
                return self.cur.rowcount

                # updateStr = ''
                # for key in updateDict:
                #     updateStr += str(key) + "= '" + str(updateDict[key]) + "',"
                # updateStr = updateStr.strip(',')
                # print updateStr

                # if not where:
                #     where = "1=1"
                #
                # updateSql = "update " + tableName + " set " + updateStr + ' where ' + where
                # self.cur.execute(updateSql)
                # return self.cur.rowcount
            self.connect.commit()  # 事务自动开启提交
        except mdb.Error, e:
            self.connect.rollback()
            print "has error %d : %s " % (e.args[0], e.args[1])
            return None
        finally:
            self.close()
        return None

    def executeSql(self, sql):
        """执行原生sql语句"""
        try:
            self.__initConnect()
            with self.connect:
                self.cur.execute(sql)
                return self.cur.rowcount
            self.connect.commit()  # 事务自动开启提交
        except mdb.Error, e:
            self.connect.rollback()
            print "has error %d : %s " % (e.args[0], e.args[1])
            return None
        finally:
            self.close()
        return None

    def deleteOne(self, tableName, where):
        """删除数据"""
        try:
            self.__initConnect()
            with self.connect:
                deleteSql = "delete from " + tableName + ' where ' + where + " limit 1"
                self.cur.execute(deleteSql)
                return self.cur.rowcount
            self.connect.commit()  # 事务自动开启提交
        except mdb.Error, e:
            self.connect.rollback()
            print "has error %d : %s " % (e.args[0], e.args[1])
            return None
        finally:
            self.close()
        return None

    def deleteAll(self, tableName, where):
        """删除数据"""
        try:
            self.__initConnect()
            with self.connect:
                deleteSql = "delete from " + tableName + ' where ' + where
                self.cur.execute(deleteSql)
                return self.cur.rowcount
            self.connect.commit()  # 事务自动开启提交
        except mdb.Error, e:
            self.connect.rollback()
            print "has error %d : %s " % (e.args[0], e.args[1])
            return None
        finally:
            self.close()
        return None

    def close(self):
        # 关闭游标 数据库连接
        if not self.cur:
            self.cur.close()
        if not self.connect:
            self.connect.close()

    # def __del__(self):
    #     try:
    #         if self:
    #             self.close()
    #     except Exception, e:
    #         logging.info("------------%s-------" % e)


__all__ = ['Mysql']
