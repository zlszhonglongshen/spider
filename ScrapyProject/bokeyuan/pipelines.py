# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs

class TutorialPipeline(object):
    def __int__(self):
        self.file = codecs.open('data.json',mode='wb',encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dump(dict(item))+"\n"
        return item
