# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 13:09:40 2018
"""

import re
import requests
import json
from urllib.parse import urlencode

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36'
}


def get_page(offset):  # 通过urlencoder建立request url
    # Request URL: https://www.toutiao.com/search_content/?offset=0&format=json&keyword=%E7%94%B5%E5%BD%B1&autoload=true&count=20&cur_tab=3&from=gallery
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '电影',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '3',
        'from': 'gallery'}
    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError:
        return None


def get_movie_url(html):  # 爬取搜索页下面下每个图集的url
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')


def parse_pic(movie_url):  # request每个图集的url
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36'
        }
        response = requests.get(movie_url, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError:
        return None


def get_pic(movie_page):  # 通过正则表达式筛选每个图片的url
    pattern = re.compile('url_list(.*?),', re.S)
    result = re.findall(pattern, movie_page)
    for i in result:
        yield (re.sub(r'\\', '', i[15:-3]))


def savefile(pic_url):  # 通过request每个图片的url，以二进制方式写入文件
    pic = requests.get(pic_url)
    pic_name = pic_url[41:] + '.jpg'
    with open(pic_name, 'wb') as f:
        f.write(pic.content)


if __name__ == '__main__':  # 遍历一定的offset页数
    for offset in range(0, 100,20):
        html = get_page(offset)
        for movie_url in get_movie_url(html):
            movie_page = parse_pic(movie_url)
            pic_urls = get_pic(movie_page)
            for pic_url in pic_urls:
                savefile(pic_url)