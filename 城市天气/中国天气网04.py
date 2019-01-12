# -*- coding: utf-8 -*-
"""
Created on 2019/1/12 10:51
@Author: Johnson
@Email:593956670@qq.com
@File: 中国天气网04.py
"""

'''
导入程序需要的程序包
'''
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import pandas as pd


def get_url(city_name): #根据城市名字获取城市代码，最终返回城市URL
    url = 'http://www.weather.com.cn/weather/'
    with open('C:\\Users\\johnson.zhong\\Documents\\GitHub\\spider\\城市天气\\city.txt', 'r', encoding='UTF-8') as fs:
        lines = fs.readlines()
        for line in lines:
            if (city_name[0] in line):
                code = line.split('=')[0].strip()
                return url + code + '.shtml'
    raise ValueError('invalid city name')


def get_data(city_name):
    url = get_url(city_name)
    resp = urlopen(url)
    print(resp)
    soup = BeautifulSoup(resp, 'html.parser')
    # print(soup)
    tagDate = soup.find('ul', class_="t clearfix")
    dates = tagDate.h1.string

    tagToday = soup.find('p', class_="tem")
    try:
        temperatureHigh = tagToday.span.string
    except AttributeError as e:
        temperatureHigh = tagToday.find_next('p', class_="tem").span.string

    temperatureLow = tagToday.i.string
    weather = soup.find('p', class_="wea").string
    tagWind = soup.find('p', class_="win")

    em = ['紫外线指数', '减肥指数', '健臻·血糖指数', '穿衣指数', '洗车指数', '空气污染扩散指数']  # 生活指数
    span = []  # 数据范围
    p = []  # 温馨提示

    star = []
    for k in soup.find('div', class_="hide show").find_all("span")[1]:  # 找到其中的star
        star.append(k)
    for i in star:  # 删除列表中不需要的元素
        if i == '\n':
            star.remove('\n')

    replace = '{}'.format(len(star)) + "颗星"  # 五颗星

    for k in soup.find('div', class_="hide show").find_all("span"):  # 找到所有标签为span
        span.append(k.text)

    span[1] = replace  # 将列表中的第二个元素替换掉

    for k in soup.find('div', class_="hide show").find_all("p"):  # 找到所有标签为span
        p.append(k.text)

    # print(em)
    # print(span)
    # print(p)

    doc = open('weather_info.txt', 'w')  # 将数据写入到固定文档

    winL = tagWind.i.string
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    days = {0:'星期一',1:'星期二',2:'星期三',3:'星期四',4:'星期五',5:'星期六',6:'星期日'}
    weekday = int(pd.Series(pd.to_datetime(now)).dt.dayofweek)
    print('今天是:{}\t{}'.format(now,days[weekday]), file=doc)
    print('风级等级：' + winL, file=doc)
    print('最低温度：' + temperatureLow, file=doc)
    print('最高温度：' + temperatureHigh + "℃", file=doc)
    print('天气：' + weather, file=doc)

    print("**********生活助手，仅供参考!!!**********", file=doc)
    for i in range(len(em)):
        print("{}\t{}\t{}".format(em[i], span[i], p[i]), file=doc)
    print("**********生活助手，仅供参考!!!**********", file=doc)


if __name__ == '__main__':
    cities = input('city name: ').split(' ')
    # print(cities)
    get_data(cities)

# for k in soup.find('div', class_="hide show"): #找到所有标签为span
#     print(k)


