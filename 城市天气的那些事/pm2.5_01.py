# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 15:53:45 2019

@author: johnson.zhong
"""

import requests
from urllib.request import urlopen
import threading
from time import ctime
from bs4 import BeautifulSoup   #besutifulsoup的第三版
import re
 
def getPM25(cityname):
    site = 'http://www.pm25.com/city/' + cityname + '.html'
    html = urlopen(site)
    soup = BeautifulSoup(html)
 
    city = soup.find("span",{"class":"city_name"})  # 城市名称
    aqi = soup.find("a",{"class":"cbol_aqi_num"})   # AQI指数
    pm25 = soup.find("span",{"class":"cbol_nongdu_num_1"})   # pm25指数
    pm25danwei = soup.find("span",{"class":"cbol_nongdu_num_2"})   # pm25指数单位
    quality = soup.find("span",{"class":re.compile('cbor_gauge_level\d$')})  # 空气质量等级
    result = soup.find("div",{"class":'cbor_tips'})   # 空气质量描述
    replacechar = re.compile("<.*?>")  #为了将<>全部替换成空
    space = re.compile(" ")
    print (city.string + u'\nAQI指数：' + aqi.string+ u'\nPM2.5浓度：' + pm25.string + pm25danwei.string + u'\n空气质量：' + quality.string + space.sub("",replacechar.sub('',str(result))))
    print ('*'*20 + ctime() + '*'*20)
 
def one_thread(cityname1):   # 单线程
    print ('One_thread Start: ' + ctime() + '\n')
    getPM25(cityname1)
 
def two_thread():   # 多线程
    print ('Two_thread Start: ' + ctime() + '\n')
    threads = []
    t1 = threading.Thread(target=getPM25,args=('beijing',))
    threads.append(t1)
    t2 = threading.Thread(target=getPM25,args=('shenyang',))
    threads.append(t2)
 
    for t in threads:
        # t.setDaemon(True)
        t.start()
       
 
if __name__ == '__main__':
 
    print ("*"*20+"welcome to 京东放养的爬虫"+"*"*20 )
    while True:
        cityname1 = input("请输入想要查看的城市名称:(例如:beijing)")
#        if cityname1 == 'quit':
#            break
        one_thread(cityname1)
    #print '\n' * 2
    #two_thread(cityname)

