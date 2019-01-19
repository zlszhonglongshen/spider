# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 14:09:34 2019

@author: johnson.zhong
"""

from bs4 import BeautifulSoup
from selenium import webdriver


def real_time_weather(url):
	
    browser = webdriver.Chrome()
    browser.get(url)
    content = browser.page_source
    browser.close()

    html = BeautifulSoup(content, "html.parser")
    tem = html.find_all("div", class_="tem")
    	# 经检查find_all方法返回的tem第一组数据为想要获取的数据
    	# span区域为实时气温的数值，em区域为实时气温的单位
    result = tem[0].span.text + tem[0].em.text
    
    print("实时气温：" + result)


if __name__ == "__main__":
    url_bj = "http://www.weather.com.cn/weather1d/101010100.shtml"
    real_time_weather(url_bj)
