# -*- coding: utf-8 -*-
"""
Created on 2019/1/22 10:33
@Author: Johnson
@Email:593956670@qq.com
@File: save_images_mongodb.py
"""
import json
import os
import re
from hashlib import md5
import pymongo
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from config import *

#引入多进程
from multiprocessing import Pool

#声明一个MongoDB数据库对象
client=pymongo.MongoClient(MONGO_URL,connect=False)
db=client[MONGO_DB]

#获取索引
def get_page_index(offset,keyword):
    data={
        'offset':offset,
        'format':'json',
        'keyword':keyword,
        'autoload':'true',
        'count': '20',
        'cur_tab':'3',
        'from': 'search_tab'
    }

    #进行编码，加上参数
    url='https://www.toutiao.com/search_content/?'+urlencode(data)
    try:
        response=requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引失败')
        return None

#解析索引页面，即搜索出来的一个个总集合。需要获取详情页面的url
def parse_page_index(html):
    try:
        #通过loads将字符串转换成对象
        data=json.loads(html)
        #使用了dict.keys()方法，返回所有键值
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    finally:
        print('解锁成功')

#获取详情
def get_page_detail(url):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        response=requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页面失败',url)
        return None

#解析获取的HTML为json格式
def parse_page_detail(html,url):
    soup=BeautifulSoup(html,'lxml')
    title=soup.select('title')[0].get_text()
    images_pattern=re.compile('gallery: JSON.parse\\((.*?)\\),',re.S)
    result=re.search(images_pattern,html)
    if result:
        #网页格式改了，需要解析2次才能正确解析
        data=json.loads(json.loads(result.group(1)))
        if data and 'sub_images' in data.keys():
            sub_images=data.get('sub_images')
            #遍历sub_images，并获取其中键值为url的数据，放入数组中
            images=[item.get('url') for item in sub_images]
            #已经获取到所有图片，循环，调用下载函数
            for image in images:download_image(image)
            return {
                'title':title,
                'url':url,
                'images':images
            }

#存储到数据库，参数采用一个字典
def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储成功',result)
        return True
    return False

#下载（注意，这里和前面不一样的是请求response.content
# content是返回二进制内容，text返回网页请求结果
#一般请求网页用text，请求图片用content
def download_image(url):
    print('正在下载：',url)
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        response=requests.get(url,headers=headers)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print('请求图片下载出错',url)
        return None

#将download_image中获取的response.text作为参数传入
def save_image(content):
    #路径包含三部分：哪个文件夹，图片名，图片后缀
    #为了防止下重复的图片，使用md5来防止
    file_path='{0}/{1}.{2}'.format('F:\\image\\',md5(content).hexdigest(),'jpg')
    #如果文件不存在，就存储下来
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()

def main(offset):
    #KEYWORD在配置文件中
    html=get_page_index(offset,KEYWORD)
    for url in parse_page_index(html):
        #此处的html是每个详情页面的内容
        html=get_page_detail(url)
        if html:
            result=parse_page_detail(html,url)
            save_to_mongo(result)

if __name__=='__main__':
    #观察头条可发现，向下拉时候会不停发出ajax请求，并且每次
    #都是参数offset偏移了20，这里多进程运行main函数，加上offset参数
    #来请求多组数据
    groups=[x*20 for x in range(1,20)]
    #声明一个进程池
    pool=Pool()
    pool.map(main,groups)

2.config.py

#存入MongoDB
MONGO_URL='localhost'
MONGO_DB='toutiao'
MONGO_TABLE='toutiao1'

#定义一个offset偏移量，用于循环
GROUP_START=1
GROUP_END=20

#搜索的关键字
KEYWORD='街拍