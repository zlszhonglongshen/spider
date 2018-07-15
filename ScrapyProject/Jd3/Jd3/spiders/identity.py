#coding:utf-8

import scrapy
from scrapy.http import Request
from ..parse import parse_info
from ..items import Jd3Item
from ..settings import PD_MAPS

class IdentitySpider(scrapy.Spider):
    name = 'identity'
    allowed_domains = ['www.jd.com']
    start_urls = []
    def start_requests(self):
        for _,url in PD_MAPS.items():
            yield Request(url)
    def parse(self, response):
        item = Jd3Item()
        ids = parse_info(response.body, 'item.jd.com.*?(\\d+)\.html', 1)
        for i in ids:
            item['info'] = i.strip()
            yield item