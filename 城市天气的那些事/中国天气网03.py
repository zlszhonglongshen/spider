# -*- coding: utf-8 -*-
"""
Created on 2019/1/12 0:08
@author: Johnson
Email:593956670@qq.com
@software: PyCharm
"""
from time import sleep

import requests
from bs4 import BeautifulSoup


def get_weather(url):
    html = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    print(soup)
    conMidtab = soup.find('div', class_='conMidtab')
    conMidtab2_list = conMidtab.find_all('div', class_='conMidtab2')
    for conMidtab2 in conMidtab2_list:
        tr_list = conMidtab2.find_all('tr')[2:]
        for index, tr in enumerate(tr_list):
            if index == 0:
                td = tr.find_all('td')
                provence = td[0].text.replace('\n', '')
                city = td[1].text.replace('\n', '')
                night_weather = td[5].text.replace('\n', '')
                min_temperature = td[7].text.replace('\n', '')
            else:
                td = tr.find_all('td')
                city = td[0].text.replace('\n', '')
                night_weather = td[4].text.replace('\n', '')
                min_temperature = td[6].text.replace('\n', '')

            print('%s 夜晚天气：%s，最低气温: %s' % (provence+city, night_weather, min_temperature))
            sleep(1)


def main():
    urls = [
        'http://www.weather.com.cn/textFC/hb.shtml',
        # 'http://www.weather.com.cn/textFC/db.shtml',
        # 'http://www.weather.com.cn/textFC/hd.shtml',
        # 'http://www.weather.com.cn/textFC/hz.shtml',
        # 'http://www.weather.com.cn/textFC/hn.shtml',
        # 'http://www.weather.com.cn/textFC/xb.shtml',
        # 'http://www.weather.com.cn/textFC/xn.shtml',
    ]
    for url in urls:
        get_weather(url)


if __name__ == '__main__':
    main()