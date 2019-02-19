# -*- coding: utf-8 -*-
"""
Created on 2019/2/19 8:53
@Author: Johnson
@Email:593956670@qq.com
@File: 搜狐动态图片.py
"""
import re
import requests
from bs4 import BeautifulSoup


#获取url_list就是所有图片的链接
def get_url(url):
    response = requests.get(url)
    response.encoding='utf-8'
    url_addr = r'<img src="(.*?)" /></p> \n<p style="text-align: center;">'
    url_list = re.findall(url_addr,response.text)
    print(url_list)
    return url_list


#下载保存所有的图片
def get_GIF(url,a):
    try:
        response = requests.get(url)
        with open("e:\\gif\\%d.gif"%a,'wb') as file:
            file.write(response.content)
    except:
        pass

#程序开始
if __name__=='__main__':
    url = 'http://www.sohu.com/a/234924456_788228'
    url_list = get_url(url)
    a=1
    for url in url_list:
        get_GIF(url,a)
        a+=1
