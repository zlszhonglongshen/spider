#coding:utf-8
import requests
import os
from bs4 import BeautifulSoup
import lxml
import sys
class DZ():
    def __init__(self,url,pageIndex):
        self.url = url+str(pageIndex)
        self.headers = {'User_Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        #得到一个的源码
    def get_one_page_html(self):
        re = requests.get(self.url,self.headers)
        html = re.text
        return html
    #得到所有的段子的URL
    def get_one_text_url(self):
        all_a = []
        for i in range(1,2):
            html = self.get_one_page_html()
            soup = BeautifulSoup(html,'lxml')
            all_h2 = soup.find_all('h2')
            for h2 in all_h2:
                all_a.append(h2.find('a').get('href'))
        return all_a
    #下载所有的段子
    def get_text(self):
        all_a = self.get_one_text_url()
        x = 0
        for a in all_a:
            re = requests.get(a,headers = self.headers)
            html = re.text
            soup = BeautifulSoup(html,'lxml')
            all_p = soup.find('article',class_='article-content').find_all('p')
            for p in all_p:
                print(p.text)


if __name__=='__main__':
    url = 'http://duanziwang.com/category/duanzi/page/'
    app = DZ(url, 2)
    app.get_text()