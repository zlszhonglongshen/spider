# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs


class W3SchoolPipeline(object):
    def __init__(self):
        self.file = codecs.open('W3School_data.json', 'wb', encoding='utf-8')  # 初始化创建一个W3School_data.json的文件
    def process_item(self, item, spider):
        line = json.dump(dict(item))+'\n' #对数据类型进行编码
        print(line)
        self.file.write(line.decode("unicode_escape"))
        return item

