'''
@Coding: 
@Author: Johnson
@Date: 2019-01-12 16:52:49
@Description: 
@Email: 593956670@qq.com
'''
# -*- coding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import pandas as pd
import  requests as rq
from selenium import webdriver



#获取城市名称以及城市的URL
def getcity():
    hotcitys = rq(url,header=header)
    soup = BeautifulSoup(hotcitys.text,'lxml') #这里使用lxml来解析
    citynames = []
    cityurls = []
    citys = soup.find_all('a',limit=19)[-10:] #分片的形式来获取十个热门城市
    for city i