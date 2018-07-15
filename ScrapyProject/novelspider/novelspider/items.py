# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bookTitle = scrapy.Field() #书的标题
    chapterNum = scrapy.Field() #书的章节
    chapterName = scrapy.Field() #书的章节名字
    chapterURL = scrapy.Field() #各章节url
    pass
