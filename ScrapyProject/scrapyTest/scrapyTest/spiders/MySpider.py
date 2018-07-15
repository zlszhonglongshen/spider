# -*- coding: utf-8 -*-
import scrapy
import urllib

from scrapytest.CourseItems import CourseItem


class MySpider(scrapy.Spider):

    name = "MySpider"

    allowed_domains = ["imooc.com"]
   
    start_urls = ["http://www.imooc.com/course/list"]

   

    def parse(self, response):
 
        item = CourseItem()
      
        for box in response.xpath('.//div[@class="course-card-container"]'):
    
            item['url'] = 'http://www.imooc.com' + box.xpath('.//@href').extract()[0]
     
            item['title'] = box.xpath('.//h3/text()').extract()[0]
   
            item['image_url'] = box.xpath('.//@src').extract()[0]
            #获取div中的学生人数
            item['student'] = box.xpath('.//div[@class="course-card-info"]/span[2]/text()').extract()[0]
            #获取div中的课程简介
            item['introduction'] = box.xpath('.//p/text()').extract()[0].strip()
            #是否有多个
            if len(box.xpath('.//div[@class="course-label"]/label/text()').extract())==1:

                item['catycray'] = box.xpath('.//div[@class="course-label"]/label/text()').extract()[0]

            elif len(box.xpath('.//div[@class="course-label"]/label/text()').extract())==2:
                item['catycray'] = box.xpath('.//div[@class="course-label"]/label/text()').extract()[0]+' '+ box.xpath('.//div[@class="course-label"]/label/text()').extract()[1]
            elif len(box.xpath('.//div[@class="course-label"]/label/text()').extract())==3:
                item['catycray'] = box.xpath('.//div[@class="course-label"]/label/text()').extract()[0]+' '+box.xpath('.//div[@class="course-label"]/label/text()').extract()[1]+' '+ box.xpath('.//div[@class="course-label"]/label/text()').extract()[2]
            else :
                item['catycray'] = ''
            
            #下载图片
            #urllib.urlretrieve(item['image_url'],'pic/'+item['title']+'.jpg')
            
            
         

            #返回信息
            yield scrapy.Request(item['url'], callback=self.parseNest,meta=item)
        
    #课程详情页
    def parseNest(self, response):
        item = response.meta
        #print item
        item['degree'] = response.xpath('.//div[@class="static-item l"]/span[@class="meta-value"]/text()').extract()[0]
         
        item['hour'] =response.xpath('.//div[@class="static-item l"]/span[@class="meta-value"]/text()').extract()[1]

        item['score']=response.xpath('.//div[@class="static-item l score-btn"]/span[@class="meta-value"]/text()').extract()[0]

        yield item

        #url跟进开始
        #获取下一页的url信息
        #url = response.xpath("//a[contains(text(),'下一页')]/@href").extract()
        #if url :
            #将信息组合成下一页的url
            #page = 'http://www.imooc.com' + url[0]
            #返回url


        for x in xrange(2,32):
            page='http://www.imooc.com/course/list?page='+str(x)
            yield scrapy.Request(page, callback=self.parse)
        #url跟进结束