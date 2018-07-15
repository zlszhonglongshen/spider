# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field

class TenxunspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    workLoction = Field()  # 工作地点
    person_number = Field()  # 招聘人数
    duty = Field()  # 职业类别
    title = Field()  # 标题
    Job_requirement = Field()  # 工作要求
    Job_duty = Field()  # 工作职责
    url = Field()  # 网页链接
    pass
