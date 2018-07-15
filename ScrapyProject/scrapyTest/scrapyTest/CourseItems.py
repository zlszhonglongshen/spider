# -*- coding: utf-8 -*-
#引入文件
import scrapy

class CourseItem(scrapy.Item):
    #课程标题
    title = scrapy.Field()
    #课程url
    url = scrapy.Field()
    #课程标题图片
    image_url = scrapy.Field()
    #课程描述
    introduction = scrapy.Field()
    #学习人数
    student = scrapy.Field()
    #课程标签
    catycray = scrapy.Field()
    #课程难度
    degree = scrapy.Field()
    #课程时长
    hour =scrapy.Field()

    #课程评分
    score=scrapy.Field()
