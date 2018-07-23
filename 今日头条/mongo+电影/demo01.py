#-*- coding: utf-8 -*-
import re
from urllib.parse import urlencode
import pymongo
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import requests
import json
import os
from hashlib import md5
# from Mongo_config import *
from multiprocessing import Pool


MONGO_URL = 'localhost'
MONGON_DB = 'toutiao'
MONGO_TABLE = 'jiepai'

# 如果没有mongodb密码就不用写数据库密码了，如果有就需要填写一下
GROUP_START = 1
GROUP_END = 20
KEYWORD = '街拍'

client = pymongo.MongoClient(MONGO_URL, connect=False)
db  = client[MONGON_DB]

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

#获取页面信息
def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1,
        'from':'gallery'
    }

    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引出错')
        return None

#索引
def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

#获取详情页信息
def get_page_detail(url):
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错', url)
        return None

# 获取页面详情
def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    # 获取标题
    title = soup.select('title')[0].get_text()
    # 图片正则表达式对象
    images_pattern = re.compile('gallery: JSON.parse\("(.*?)"\)', re.S)
    result = re.search(images_pattern, html)
    # 替换不需要的数据
    json_images = re.sub(r'\\{1,2}', '', result.group(1))
    if  result:
         images_data = json.loads(json_images)
         if images_data and 'sub_images' in images_data.keys():
             sub_images = images_data.get('sub_images')
             # 转换成数组
             images = [item.get('url') for item in sub_images]
             # 下载图片
             for image in images: down_load_images(image)
             return{
                'title': title,
                'url': url,
                'images': images
             }

# 下载图片
def down_load_images(url):
    print('正在下载',url)
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            save_images(response.content)
        return None
    except RequestException:
        print('请求图片出错', url)
        return None

# 存储图片
def save_images(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()

# 存储到mongoDB
def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储成功', result)
        return True
    return False

def main(offset):
    html = get_page_index(offset, KEYWORD)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html, url)
            if result: save_to_mongo(result)
            print(result)

if __name__ == '__main__':
    groups = [x*20 for x in range(GROUP_START, GROUP_END + 1)]
    pool = Pool()
    pool.map(main, groups)

