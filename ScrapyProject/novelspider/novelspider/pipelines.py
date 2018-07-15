# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#导入了3个模块
#导入了3个模块
from items import NovelspiderItem          ## 链接item
from scrapy.conf import settings
#from scrapy import settings         #  不出错
import pymongo

class NovelspiderPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']                ## settings 赋值piplines
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']   ## 数据库名字
        client = pymongo.MongoClient(host = host,port = port)   #链接数据库
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]
        print 'piplines'

    def process_item(self, item, spider):
        bookInfo = dict(item)    #把item转换为字典
        self.post.insert(bookInfo)    # 把数据存入到bookInfo字典里,插入数据库
        return item