# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import sys
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spider import CrawlSpider,Rule
from JD.items import TutorialItem

class ListSpider(CrawlSpider):
    #爬虫名称
    name = "tutorial"
    #设置下载延时
    download_delay = 1
    #允许域名
    allowed_domains = ["news.cnblogs.com"]
    #开始URl
    start_urls = ["https://news.cnblogs.com"]
    #爬虫规则
    rules = (
    Rule(SgmlLinkExtractor(allow=(r'https://news.cnblogs.com/n/page/\d',))),
    Rule(SgmlLinkExtractor(allow=(r'https://news.cnblogs.com/n/\d+',)), callback='parse_content'),)
    #解析内容
    def parse_content(self,response):
        item = TutorialItem()
        #当前url
        title = response.selector.xpath('//div[@id="news_title"]')[0].extract().decode('utf-8')
        item['title'] = title
        author = response.selector.xpath('//div[@id="news_info"]/span/a/text()')[0].extract().decode('utf-8')
        item['author'] = author
        releasedate = response.selector.xpath('//div[@id="news_info"]/span[@class="time"]/text()')[0].extract().decode('utf-8')
        item['releasedate'] = releasedate
        yield item
