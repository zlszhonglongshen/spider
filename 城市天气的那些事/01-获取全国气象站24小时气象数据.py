# -*- coding: utf-8 -*-
"""
Created on 2019/1/13 0:34
@author: Johnson
Email:593956670@qq.com
@software: PyCharm
"""
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = 'http://www.weather.com.cn/weather1d/101200101.shtml'
html = urlopen(url).read()
# print(html)

'''
接下来就是解析数据
'''
soup  = BeautifulSoup(html,'html.parser',from_encoding='utf-8')
res_data = soup.findAll('script') #获取页面内的所有<Script>标签
weather_data = res_data[4] #获取第5个标签，返回一个list
for x in weather_data: #取list的第一个
    weather1 = x
index_start = weather1.find("{") #目前weather还是一个字符串，需要将里面的json截取出来
index_end = weather1.find(";")
weather_str = weather1[index_start:index_end]
weather = eval(weather_str) #将字符串转化为json

weather_dict = weather["od"]
weather_date = weather_dict["od0"]   #时间
weather_position_name = weather_dict["od1"] #地点
weather_list = list(reversed(weather["od"]["od2"]))
insert_list = []                     #存放每小时的数据的list，用于之后插入数据库
for item in weather_list:
  #od21小时，od22温度，od26降雨，od24风向，od25风力
  weather_item = {}
  weather_item['time'] = item['od21']
  weather_item['temperature'] = item['od22']
  weather_item['rain'] = item['od26']
  weather_item['humidity'] = item['od27']
  weather_item['windDirection'] = item['od24']
  weather_item['windPower'] = item['od25']
  weather_item['od23'] = item['od23']
  insert_list.append(weather_item)

#打印查看变量
print("weather_date:",weather_date)
print("weather_position_name:",weather_position_name)
print("weather_list:",weather_list)
print ("insert_list:",insert_list)

# 作者：oshimaRyu
# 链接：https://www.jianshu.com/p/ca37900a25e6
# 來源：简书
# 简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。