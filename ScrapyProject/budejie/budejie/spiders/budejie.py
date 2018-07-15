#coding:utf-8
# 引入需要的模块
import scrapy
from ..items import BudejieItem
class BudejieSpider(scrapy.Spider):
    name='baisibudejie'
    allowed_domains=['budejie.com']
    start_urls=['http://www.budejie.com/text/2']

    def parse(self,response):
        '''
        在这个函数中不做任何数据处理，只是将第一个url加入到urljoin中
        并将请求对象交给parse_response进行数据处理
        :param response:
        :return:
        '''
        url=response.urljoin(self.start_urls[0])
        yield scrapy.Request(url,callback=self.parse_response)

    def parse_response(self,response):
        '''
        在这个函数中才是真的数据处理，将筛选后的数据逐个交给pipelines管道模块进行存储
        :param response:
        :return:
        '''
        # 1.将数据保存在本地表格文件，一般用于测试
        # 定义一个列表，专门用于保存段子内容
        content_list=[]
        # 使用xpath对段子内容进行过滤、筛选
        contents= response.xpath("//div[@class='j-r-list-c']/div[@class='j-r-list-c-desc']/a").xpath("string(.)").extract()
        for content in contents:
            new_item=BudejieItem()
            new_item['content']=content
            content_list.append(new_item)
            yield new_item


        # 将第一页的数据爬取筛选完毕后，筛选页面链接/a/@href,.extract()是将选择器对象转换成Unicode对象
        page_list=response.xpath("//div[@class='m-page m-page-sr m-page-sm']/a/@href").extract()

        for page in page_list:
            # 将路由交由urljoin（）管理，去重
            url=response.urljoin(page)
            # 创建新的请求对象，交由自己处理，递归，依次筛选数据，并yield交给管道模块
            yield scrapy.Request(url,callback=self.parse_response)