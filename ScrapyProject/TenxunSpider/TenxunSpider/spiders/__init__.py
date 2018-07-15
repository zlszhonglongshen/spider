# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule,CrawlSpider
from Tenxunspider.items import TenxunspiderItem
from scrapy.linkextractors import LinkExtractor
class TenxunSpider(CrawlSpider):
    name = "tenxun"
    #allowed_domains = ["Tencent.com"]
    start_urls = ['http://hr.tencent.com/position.php']
    rules={
        Rule(LinkExtractor(allow='position\.php',restrict_xpaths="//div[@class='pagenav']"),follow=True),
        Rule(LinkExtractor(allow="position_detail\.php",restrict_xpaths="//td[@class='l square']"),follow=False,callback="paser_item")
    }
    def paser_item(self,response):
        item=TenxunspiderItem()
        print (response.url)
        item['title']=response.xpath("//tr[@class='h']/td/text()").extract()
        item['workLoction']=response.xpath("//tr[@class='c bottomline']/td[1]/text()")[0].extract()
        item['person_number']=response.xpath("//tr[@class='c bottomline']/td[3]/text()").re('(\d+)')[0]
        item["duty"]=response.xpath("//tr[@class='c bottomline']/td[2]/text()")[0].extract()
        item['url']=response.url
        item["Job_requirement"]=response.xpath("//tr[@class='c']")[1].xpath('//li/text()').extract()
        item["Job_duty"]=response.xpath("//tr[@class='c']")[0].xpath('//li/text()').extract()
        yield item