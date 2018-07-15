#encoding:utf-8
import scrapy
import re
from scrapy.selector import Selector
from ..items import Tech163ItemItem
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule
class Spider(CrawlSpider):
  name = 'news'
  allowed_domains = ["tech.163.com"]
  start_urls = ['http://tech.163.com/']
  