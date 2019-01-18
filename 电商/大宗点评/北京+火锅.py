# -*- coding:utf-8 -*-
import re
from bs4 import BeautifulSoup
import json
import threading
from requests import Session
class dazp_bj:
    def __init__(self,category):
        self.baseUrl='http://www.dianping.com'
        self.bgurl=category[0]
        self.typename=category[1]
        self.page=1
        self.pagenum=10 #设置最大页面数目，大众点评每个条目下最多有50页，可以根据自己需求进行设置
        self.headers={
			"Host":"www.dianping.com",
			"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0",
			#此User-Agent是我本人的参数，在使用时记得修改为自己的参数，如何获取下四.4部分有讲解
                "Referer":"http://www.dianping.com/beijing",}
    def start(self):
        self.s=Session()	#定义一个Session()对象
        print(self.bgurl,self.typename)
        print("please wait for 15")
        dazp_bj.__parseHtml(self,self.bgurl) #调用__parseHtml函数
    def __parseHtml(self,preurl):
        _json=dict()	#定义一个字典用以存储数
        html=self.s.post(preurl,headers=self.headers).text	#发送请求，获取html
        soup=BeautifulSoup(html,'lxml') #进行解析
        name=['商家名称','评论数量','人均消费','地址','评分','链接']
        for li in soup.find('div',class_="shop-wrap").find('div',id="shop-all-list").ul.find_all('li'):
            info=li.find('div',class_='txt')
            _json[name[0]]=info.find('div',class_='tit').a.h4.get_text().encode('utf-8')
            _json[name[1]]=int(info.find('div',class_='comment').find('a',class_="review-num").b.get_text().encode('utf-8'))
            _json[name[2]]=int(re.sub('￥','',info.find('div',class_='comment').find('a',class_="mean-price").b.get_text().encode('utf-8')))
            _json[name[3]]=info.find('div',class_='tag-addr').find('span',class_='tag').get_text().encode('utf-8')+info.find('div',class_='tag-addr').find('span',class_='addr').get_text().encode('utf-8')
            _json[name[4]]=float(info.find('span',class_='comment-list').find_all('b')[0].get_text())+float(info.find('span',class_='comment-list').find_all('b')[1].get_text())+float(info.find('span',class_='comment-list').find_all('b')[2].get_text())
            _json[name[5]]=self.baseUrl+info.find('div',class_='tit').a['href']
            with open(self.typename+'.json','a') as outfile:
                json.dump(_json,outfile,ensure_ascii=False)
            with open(self.typename+'.json','a') as outfile:
                outfile.write(',\n')
        self.page+=1
        if self.page<=self.pagenum:
            self.nexturl=self.baseUrl+soup.find('div',class_='page').find('a',class_='next')['href']  #获得下一页的链接
            dazp_bj.__parseHtml(self,self.nexturl)
if __name__=='__main__':
    cat=[(r'http://www.dianping.com/search/category/2/10/g110',u'火锅 ')]
    obj=list()
    obj.append(dazp_bj(cat[0]))
    [threading.Thread(target=foo.start(),args=()).start for foo in obj]#多线程执行obj列表中的任务