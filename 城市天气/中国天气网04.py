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
import  requests
from selenium import webdriver


def get_url(city_name): #根据城市名字获取城市代码，最终返回城市URL
    url = 'http://www.weather.com.cn/weather/'
    with open('C:\\Users\\johnson.zhong\\Documents\\GitHub\\spider\\城市天气\\city.txt', 'r', encoding='UTF-8') as fs:
        lines = fs.readlines()
        for line in lines:
            if (city_name[0] in line):
                code = line.split('=')[0].strip()
                return code,url + code + '.shtml'
    raise ValueError('invalid city name')


def get_html(url):
    '''
    封装请求
    '''
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'ContentType':
        'text/html; charset=utf-8',
        'Accept-Encoding':
        'gzip, deflate, sdch',
        'Accept-Language':
        'zh-CN,zh;q=0.8',
        'Connection':
        'keep-alive',
    }
    try:
        htmlcontet = requests.get(url, headers=headers, timeout=30)
        htmlcontet.raise_for_status()
        htmlcontet.encoding = 'utf-8'
        return htmlcontet.text
    except:
        return " 请求失败 "


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
    return result

def getPM25(doc):
    site = 'http://www.pm25.com/city/' + 'guangzhou' + '.html'
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
    print('AQI指数:' + aqi.string+'\t'+ 'PM2.5浓度:' + pm25.string +'\t'+ pm25danwei.string + '空气质量:' + quality.string+'\t' + space.sub("",replacechar.sub('',str(result))),file=doc)
 

def get_data(city_name):
    code,url = get_url(city_name)
    url2 = 'http://www.weather.com.cn/weather1d/{}.shtml'.format(code)
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

    # tem = soup.find_all(class_="tem")[0].text.strip()
    # print("当前温度:", tem)

    # html = get_html(url2)
    # soup2 = BeautifulSoup(html, 'lxml')
    # content_ul = soup2.find('div', class_='t').find('ul', class_='clearfix').find_all('li')
    # weather_list = []
    # for content in content_ul:
    #     try:
    #         weather_temp = {}
    #         weather_temp['day'] = content.find('h1').text
    #         weather_temp['temperature'] = content.find(
    #             'p', class_='tem').span.text + content.find(
    #                 'p', class_='tem').em.text
    #         weather_list.append(weather_temp)
    #     except:
    #         print('查询不到')
    # print({'实时温度：{}'.format(weather_list)},doc)


    winL = tagWind.i.string
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    days = {0:'星期一',1:'星期二',2:'星期三',3:'星期四',4:'星期五',5:'星期六',6:'星期日'}
    weekday = int(pd.Series(pd.to_datetime(now)).dt.dayofweek)

    result = real_time_weather(url2)

    print('今天是:{}\t{}'.format(now,days[weekday]), file=doc)
    print('天气：' + weather, file=doc)
    print("现在气温：" + result,file=doc)
    print('最低温度：' + temperatureLow, file=doc)
    print('最高温度：' + temperatureHigh + "℃", file=doc)
    print('风级等级：' + winL, file=doc)

    print("**********生活助手，仅供参考!!!**********", file=doc)
    print("{}\t{}\t{}".format("生活指标","等级","生活Tips")+"\n", file=doc)
    for i in range(len(em)):
        print("{}\t{}\t{}".format(em[i], span[i], p[i]), file=doc)
    # print("\n", file=doc)
    getPM25(doc) #获取PM2.5的相关信息

    print("**********生活助手，仅供参考!!!**********", file=doc)

    


if __name__ == '__main__':
    cities = input('city name: ').split(' ')
    # print(cities)
    get_data(cities)

# for k in soup.find('div', class_="hide show"): #找到所有标签为span
#     print(k)


