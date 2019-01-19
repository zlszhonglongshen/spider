# -*- coding: utf-8 -*-
"""
Created on 2019/1/13 0:44
@author: Johnson
Email:593956670@qq.com
@software: PyCharm
"""
import pymysql
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time

conn = pymysql.connect(host='172.20.71.35', port=3306, user='root', passwd='root', db='mysql', charset='utf8mb4')

c = conn.cursor()

c.execute('''create table weather
            (positionId varchar(20),
            name varchar(20),
            date_time varchar(20) ,
            temperature varchar(20),
            rain varchar(20),
            humidity varchar(20),
            windDirection varchar(20),
            windPower varchar(20),            
            fullName varchar(50) 
            );''')


def getPositionName(soup, num):  #soup：beautiful的soup对象，num城市编码
    position_name = soup.find(class_="crumbs")
    name = []
    for i in range(len(position_name.find_all("a"))):
        name.append(position_name.find_all("a")[i].text)
    name.append(position_name.find_all("span")[len(position_name.find_all("span"))-1].text)
    # [0].text, position_name.find_all("a")[1].text,position_name.find_all("span")[1].text,position_name.find_all("span")[2].text
    name_str = "-".join(name)
    print(name_str)
    return name_str

def spider(url,num): #url，num：城市编码
    try:
        html = urlopen(url).read()
        soup = BeautifulSoup(html,'html.parser',from_encoding='utf-8')
        res_data = soup.findAll('script')
        weather_data = res_data[4]
        fullName = getPositionName(soup, num)
        for x in weather_data:
            weather1 = x
        index_start = weather1.find("{")
        index_end = weather1.find(";")
        weather_str = weather1[index_start:index_end]
        weather = eval(weather_str)
        weather_dict = weather["od"]
        weather_date = weather_dict["od0"]
        weather_position_name = weather_dict["od1"]
        weather_list = list(reversed(weather["od"]["od2"]))

        #将数据存入数据库
        save_in_db(num,weather_date, weather_position_name, weather_list, fullName)
    except:
        pass
    return True

def save_in_db(num,weather_date, weather_position_name, weather_list, fullName):
    insert_list = []
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
    conn = pymysql.connect(host='172.20.71.35', port=3306, user='root', passwd='root', db='mysql', charset='utf8mb4')
    c = conn.cursor()
    for item in insert_list:
        c.execute("insert into weather (positionId,name,date_time,temperature,rain,humidity,windDirection,windPower,fullName) \
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(str(num),weather_position_name,item['time'],item['temperature'],item['rain'],item['humidity'],item['windDirection'],item['windPower'],fullName))
    conn.commit()
    conn.close()

def start():
    base_url = "http://www.weather.com.cn/weather1d/101"
    province_num = 1
    while (province_num < 80):
        flag = True
        city_num = 1
        while (city_num < 20):
            position_num = 1
            while (position_num < 30):
                num_str = str(province_num).zfill(2) + str(city_num).zfill(2) + str(position_num).zfill(2)
                url = base_url + num_str + ".shtml"
                time.sleep(2)
                print(url,num_str)
                flag = spider(url, num_str)
                if (flag == False):
                    break
                position_num += 1
                pass
            if (flag == False and position_num == 1):
                break
            city_num += 1
            pass
        if (flag == False and position_num == 1 and city_num == 1):
            break
        province_num += 1

if __name__ == "__main__":
    # spider("http://www.weather.com.cn/weather1d/101200101.shtml",101200101)
    start()