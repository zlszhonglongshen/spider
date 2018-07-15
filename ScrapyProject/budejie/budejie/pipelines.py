# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymysql
pymysql.install_as_MySQLdb()
class BudejiePipeline(object):
    def __init__(self):
        '''
        初始化函数，与数据库建立连接
        '''
        self.engine=create_engine('mysql://root:root@localhost/mysql?charset=utf8mb4')
        Session=sessionmaker(bind=self.engine)
        self.session=Session()

    def close_spider(self,spider):
        '''
        在爬虫程序关闭调用的函数,关闭数据库的连接

        :param spider:
        :return:

        '''
        # 在关闭与数据库连接之前确保所有的sql语句已经提交
        self.session.commit()
        self.session.close()
    def process_item(self, item, spider):
        '''
        核心处理函数，专门处理爬虫程序中已经封装好的item对象
        :param item:
        :param spider:
        :return:
        '''
        print('正在保存数据')
        sql="insert into budejie(content) values('%s')"%item['content']
        # 执行sql语句
        self.session.execute(sql)