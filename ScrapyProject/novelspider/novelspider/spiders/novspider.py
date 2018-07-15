#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

'''
Spider是一个继承自scrapy.contrib.spiders.CrawlSpider的Python类，有三个必需的定义的成员
name: 名字，这个spider的标识
start_urls:一个url列表，spider从这些网页开始抓取
parse():一个方法，当start_urls里面的网页抓取下来之后需要调用这个方法解析网页内容，同时需要返回下一个需要抓取的网页，或者返回items列表
所以在spiders目录下新建一个spider，novelspider.py:

'''

# 导入3个模块  一个CrawlSpider   一个selector   一个导入item类的模块
# from scrapy.spiders import CrawlSpider
from scrapy.contrib.spiders import CrawlSpider

# from scrapy.selector import Selector           # 出错：没有该模块  更换下面这个模块XpathSelector
from scrapy.selector import XPathSelector  # 导入不出错
from novelspider.items import NovelspiderItem  # 导入item中的类NovelspiderItem

# from scrapy.selector import HtmlXPathSelector


class novSpider(CrawlSpider):
    name = "novspider"  # name ,spider标识 唯一
    redis_key = 'nvospider'
    start_urls = ['http://www.daomubiji.com/']  # spider从这里开始爬取网页

    def parse(self, response):
        selector = XPathSelector(response)  # 获取网页源代码
        print '爬取源码完毕。。。'
        table = selector.select('//table')  ##  查找书及其内容所在位置，获取书的名字

        for each in table:
            bookName = each.select('tr/td[@colspan="3"]/center/h2/text()').extract()[0]
            content = each.select('tr/td/a/text()').extract()  # 章节名称
            url = each.select('tr/td/a/@href').extract()  # 章节网址
            # print type(bookName)
        # print content      # 列表
        for i in range(len(url)):
            item = NovelspiderItem()  # 链接item
            item['bookName'] = bookName
            item['chapterURL'] = url[i]  ## 赋值给item中定义的chapterurl
            ###  防止报错
            try:
                item['bookTitle'] = content[i].split(' ')[0]
                item['chapterNum'] = content[i].split(' ')[1]
            except Exception, e:
                continue

            try:
                item['chapterName'] = content[i].split(' ')[2]
            except Exception, e:
                item['chapterName'] = content[i].split(' ')[1][-3:]
            yield item