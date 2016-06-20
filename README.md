# spider
本项目主要抓取rss订阅或根据后台配置规则抓取指定网站

## 后台配置截图如下

[![配置列表](http://img.tobabel.cn/2016/06/08/spider_list.png)](http://img.tobabel.cn/2016/06/08/spider_list.png)
[![配置详情](http://img.tobabel.cn/2016/06/08/spider_detail.png)](http://img.tobabel.cn/2016/06/08/spider_detail.png)


## 配置文件 config.py
  debug_on          是否开启log
  OPEN_MD5_CHECK    是否开启md5校验
  REQUEST_TIME_OUT  http请求超时设置 
  MAIN_LOOP_SLEEP_TIME    主循环休眠时间
  SPIDER_MAX_POOL_NUM     runspider线程池大小  
  RSS_MAX_POOL_NUM        RSS线程池大小
  RUN_SYNC_INTERVAL_TIME  多久同步一次数据到线上，单位秒
  SYNC_RECORDS_NUMS       一次同步多少条数据
  REFERER                 referer
  ENCRYPT_MD5_KEY         http通信密钥
  
### 数据库配置
  db_host                 host,eg:'127.0.0.1'
  db_user                 数据库用户名 eg : 'root'
  db_password             数据库密码
  db_name                 数据库名称
  db_table_name           临时存储抓取数据表 



## 目录结构

```

├── config.py                                  配置文件
├── mySpiders                                  爬虫项目文件夹
│   ├── contrib                                重写scrapy user agent 中间件
│   │   ├── downloadmiddleware
│   │   │   ├── __init__.py
│   │   │   ├── rotate_useragent.py
│   │   ├── __init__.py
│   ├── __init__.py
│   ├── items.py
│   ├── pipelines.py                           pipeline文件
│   ├── Redis                                  redis相关模块
│   │   ├── __init__.py
│   │   ├── redisTest.py
│   │   └── RequstDistinctRedis.py
│   ├── rsa                                    RSA模块
│   │   ├── private_key.pem
│   │   ├── public_key.pem
│   │   └── RSA.py
│   ├── settings.py
│   ├── spiders                                爬虫具体实现
│   │   ├── BaseFeed.py
│   │   ├── CommonCrawlSpider.py
│   │   ├── CommonFeedRss.py
│   │   ├── CommonXmlFeed.py
│   │   ├── CrawlSpider.py
│   │   ├── ImageSpider.py
│   │   ├── __init__.py
│   │   ├── MyBaseSpider.py
│   │   ├── stackoverflow_spider.py
│   │   ├── WeChatSpider.py
│   │   ├── XmlFeedSpider.py
│   ├── sql                                    mysql相关模块
│   │   ├── AactiveRecord.py
│   │   ├── connect.py
│   │   ├── __init__.py
│   │   ├── mysql.py
│   │   ├── syncCrawlInfos.py
│   │   └── test.py
│   └── utils                                  小助手模块
│       ├── CollectionHelper.py
│       ├── convert.py
│       ├── hash.py
│       ├── http.py
│       ├── httpRequest.py
│       ├── http_test.py
│       ├── __init__.py
│       ├── iterable2string.py
│       ├── log.py
│       └── time.py
├── rss.py                                    rss爬虫运行入口
├── runSpider.py
├── scrapy.cfg
├── start.py                                  通用爬虫运行入口
├── syncDagrame.py                            数据同步脚本

```  


## 脚本运行入口
  rss.py       运行爬虫，抓取rss订阅源
  start.py     运行爬虫，根据后台配置规则抓取指定网站
  syncDagrame  同步本地抓取数据到线上
  

## 本项目需要结合后台系统才能运行，暂时不提供测试服务器

