#coding:utf-8
import scrapy
from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from job_51.items import  Job51Item

class DemoSpider(CrawlSpider):
    name = 'demo'
    start_urls = [
        "http://search.51job.com/list/000000,000000,0000,00,9,99,php,2,1.html?lang=c&degreefrom=99&stype=&workyear=99&cotype=99&jobterm=99&companysize=99&radius=-1&address=&lonlat=&postchannel=&list_type=&ord_field=&curr_page=&dibiaoid=0&landmark=&welfare=",
        "http://search.51job.com/list/000000,000000,0000,00,9,99,Python%25E5%25BC%2580%25E5%258F%2591%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
        ]
    rules = {
        Rule(LinkExtractor(allow="http:\/\/search.51job.com\/list\/", restrict_xpaths="//div[@class='p_in']"),
             callback="paser_item", follow=True),
        # Rule(LinkExtractor(allow=""))
    }
    def parse_item(self, response):
        divs = response.xpath("//dic[@class='el']")
        item = Job51Item()
        print('ip{0}'.format(response.meta['proxy']))
        for div in divs:
            try:
                item['duty'] = div.xpath("./p/span/a/text()")[0].extract().strip()
                item['time'] = div.xpath("./span[4]/text()").extract()
                item['name'] = div.xpath("./span[1]/a/text()").extract()
                item['location'] = div.xpath("./span[2]/text()").extract()
                item['sallary'] = div.xpath("./span[3]/text()").extract()
                yield item
            except Exception:
                pass