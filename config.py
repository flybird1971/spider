#!/usr/bin/env python
# coding:utf8

# 是否关闭log
debug_on = True

# 主循环 休眠时间
MAIN_LOOP_SLEEP_TIME = 6

# runspider 线程池
SPIDER_MAX_POOL_NUM = 3

# http通信密钥
ENCRYPT_MD5_KEY = '9b4fc52bc7208cd618195abee8d57ad6'

# 单个spider 初始化start_urls数目
MAX_START_URLS_NUM = 1

# 判断url是否重复
requst_distinct_url = 'http://www.babel.com/api/cluster-requst-distinct/index'

# 判断队列长度
requst_length_url = 'http://www.babel.com/api/get-spider-rules/get-length'

# 获取爬虫规则
request_url = 'http://www.babel.com/api/get-spider-rules/get'

# 数据库配置
db_host = '127.0.0.1'
db_user = 'root'
db_password = '123456'
db_name = 'babel'
db_table_name = 'bb_crawl_infos'
