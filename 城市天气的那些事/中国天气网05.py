# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 13:19:35 2019

@author: johnson.zhong
"""

'''
抓取每天的天气数据
python 3.6.2
url:http://www.weather.com.cn/weather1d/101190401.shtml
'''
import json
import requests
import bs4

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

def get_content(url):
    '''
    抓取页面天气数据
    '''
    weather_list = []
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    content_ul = soup.find('div', class_='t').find('ul', class_='clearfix').find_all('li')
    for content in content_ul:
        try:
            weather = {}
            weather['day'] = content.find('h1').text
            weather['temperature'] = content.find(
                'p', class_='tem').span.text + content.find(
                    'p', class_='tem').em.text
            weather_list.append(weather)
        except:
            print('查询不到')
    print(weather_list)

if __name__ == '__main__':
    url = 'http://www.weather.com.cn/weather1d/101190401.shtml'
    get_content(url)