#!/usr/bin/env python
#coding:utf-8

from mysql import Mysql




if __name__ == '__main__':   

    import time,json
    config = {'host':'127.0.0.1','user':'root','passwd':'123456'}
    database = 'babel'
    db =  Mysql(config,database)
    tableName = 'bb_crawl_infos'
    with open('../../log.insert.sql','r+') as f:
        d = f.read()
        d = json.loads(d)
        # print d
        db.insert(tableName,d)
        # infos = json.dumps(dict(insertData))
     



    # sql = 'select * from bb_spider_rules' 
    # print db.findOne(sql)
    # for i in db.findAll(sql):
    #     print i
    #     print "*"*88
    
    # tableName = 'bb_crawl_infos'
    # insertData = {
    #     'source_url' : 'www.baidu.com',
    #     'unique_code' : 'eesaaaaa',
    #     'rule_id' : '2',
    #     'title' : 'testttitle',
    #     'description' : 'testdescription',
    #     'public_time' : int(time.time()),
    #     'create_time' : int(time.time())
    # }
    # # db.insert(tableName,insertData)

    # fieldTuple = ('source_url','unique_code','rule_id','title','description','public_time','create_time')
    # insertDataList = [
    #     ('www.baidu.com','Qeatwtlesaa','2','twtle','testdescription',int(time.time()),int(time.time())),
    #     ('www.baidu.com','Qeatatstitlesaa','2','tatstitle','testdescription',int(time.time()),int(time.time())),
    #     ('www.baidu.com','Qeawwitlesaa','2','wwitle','testdescription',int(time.time()),int(time.time())),
    #     ('www.baidu.com','Qeaaettitlesaa','2','aettitle','testdescription',int(time.time()),int(time.time())),
    #     ('www.baidu.com','Qeaaftlesaa','2','aftle','testdescription',int(time.time()),int(time.time())),
    # ]
    # print db.batchInsert(tableName,fieldTuple,insertDataList)

    # updateDict = {
    #     'source_url' : 'www.baidu.com',
    #     'rule_id' : '121',
    #     'description' : 'aa'
    # }
    # print db. update(tableName,updateDict,'id>12')
    

    # print db.deleteOne(tableName,'id>12')

    # print db.deleteAll(tableName,'id>12')