# -*- coding: utf-8 -*-
"""
Created on 2019/1/18 22:51
@Author: Johnson
@Email:593956670@qq.com
@File: final_work.py
"""
# -*- coding: utf-8 -*-
"""
Created on 2019/1/18 17:41
@Author: Johnson
@Email:593956670@qq.com
@File: GetMessage_final.py
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import datetime
import pandas as pd
import requests
from selenium import webdriver
from wxpy import *
from threading import Timer
import itchat as ic
import time
from lxml.html import etree
import time

def startPro():
    while(1):
        currentHour = int(time.strftime("%H"))
        print(currentHour)
        if currentHour==7:
            print("It's time")
            break
        if currentHour == 6:
            print("itstimerightnow")
            time.sleep(60)
        else:
            print("It's not time ,sleep........")
            time.sleep(3500)


def get_url(city_name):  # 根据城市名字获取城市代码，最终返回城市URL
    url = 'http://www.weather.com.cn/weather/'
    with open('C:\\Users\\johnson.zhong\\Documents\\GitHub\\spider\\城市天气的那些事\\city.txt', 'r', encoding='UTF-8') as fs:
        # with open('/work/johnson_folder/city.txt', 'r', encoding='UTF-8') as fs:
        lines = fs.readlines()
        for line in lines:
            if (city_name[0] in line):
                code = line.split('=')[0].strip()
                return code, url + code + '.shtml'
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


def getPM25():
    site = 'http://www.pm25.com/city/' + 'guangzhou' + '.html'
    html = urlopen(site)
    soup = BeautifulSoup(html, 'html.parser')

    city = soup.find("span", {"class": "city_name"})  # 城市名称
    aqi = soup.find("a", {"class": "cbol_aqi_num"})  # AQI指数
    pm25 = soup.find("span", {"class": "cbol_nongdu_num_1"})  # pm25指数
    pm25danwei = soup.find("span", {"class": "cbol_nongdu_num_2"})  # pm25指数单位
    quality = soup.find("span", {"class": re.compile('cbor_gauge_level\d$')})  # 空气质量等级
    result = soup.find("div", {"class": 'cbor_tips'})  # 空气质量描述
    replacechar = re.compile("<.*?>")  # 为了将<>全部替换成空
    space = re.compile(" ")
    return quality.string,space.sub("", replacechar.sub('', str(result))).replace("\n"+"温馨提示："+"\n","")


def get_data(city_name):
    code, url = get_url(city_name)
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


    winL = tagWind.i.string
    now = datetime.now().strftime('%Y-%m-%d')
    days = {0: '星期一', 1: '星期二', 2: '星期三', 3: '星期四', 4: '星期五', 5: '星期六', 6: '星期日'}
    weekday = int(pd.Series(pd.to_datetime(now)).dt.dayofweek)

    return now,days[weekday],weather,temperatureLow,temperatureHigh,winL,getPM25()
    # print("**********生活助手，仅供参考!!!**********", file=doc)
    # print("{}\t{}\t{}".format("生活指标", "等级", "生活Tips") + "\n", file=doc)
    # for i in range(len(em)):
    #     print("{}\t{}\t{}".format(em[i], span[i], p[i]), file=doc)

def start():
    # 星座运势
    response = requests.get('https://www.xzw.com/fortune/taurus/')
    response2 = requests.get('https://www.xzw.com/fortune/scorpio/')
    if not response.status_code == 200:
        print('星座运势请求错误：' + str(response.status_code))
    sel =etree.HTML(response.text)
    fortune = sel.xpath('//div[@class="c_box"]/div[@class="c_cont"]/p/span/text()')[0]
    sel2 =etree.HTML(response2.text)
    fortune2 = sel2.xpath('//div[@class="c_box"]/div[@class="c_cont"]/p/span/text()')[0]
    return fortune,fortune2


try:
    now,weekday,weather,temperatureLow,temperatureHigh,winL,getPM25 = get_data("广州".split(' '))
    xingzuo_chunv,xingzuo_tianxie = start()
    message = "今天是："+now+ "\n" +"星期："+ weekday + "\n" + "天气："+weather \
              + "\n"+ "温度："+temperatureLow + "-"+ temperatureHigh+"℃"+ "\n"+"空气质量："+getPM25[0]+\
              getPM25[1]+"风力等级："+winL + "\n"
    print(message)
except:  # 抛出异常
    message = ""
    print("Get message failed")
ic.auto_login(hotReload=True)

# users = ic.search_friends(name='Ruby')
# users = ic.search_friends(name='Johnson')
# users = ic.search_chatrooms(name="Test")
# # users = ic.search_friends(name="无限极数据科学")
# userName = users[0]['UserName']


names = ["Test","无限极数据科学"]
userName = []

for i in names:
    try:
        if len(ic.search_friends(name=i))!=0:
            NameTemp = ic.search_friends(name=i)[0]['UserName']
            userName.append(NameTemp)
        else:
            NameTemp = ic.search_chatrooms(name=i)[0]['UserName']
            userName.append(NameTemp)
    except:
        pass

def job():
    for i in userName:
        ret = ic.send(msg=message, toUserName=i)
        if ret:
            print("Succeed Sending")
        else:
            print("Error sending")
    time.sleep(10)
        # t = Timer(30,job)
        # t.start()

if __name__ == '__main__':
    job()