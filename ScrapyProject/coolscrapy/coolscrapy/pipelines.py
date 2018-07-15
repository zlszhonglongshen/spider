# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import redis
import json
import logging
from contextlib import contextmanager
from scrapy import signals
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from sqlalchemy.orm import sessionmaker
from coolscrapy.models import News, db_connect, create_news_table, Article
class ArticleDataBasePipeline(object):
    """保存文章到数据库"""
    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)
    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        pass
    def process_item(self, item, spider):
        a = Article(url=item["url"],
                    title=item["title"].encode("utf-8"),
                    publish_time=item["publish_time"].encode("utf-8"),
                    body=item["body"].encode("utf-8"),
                    source_site=item["source_site"].encode("utf-8"))
        with session_scope(self.Session) as session:
            session.add(a)
    def close_spider(self, spider):
        pass