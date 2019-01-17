#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author;Tsukasa

import json
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import pymongo


def generate_allurl(user_in_nub, user_in_city):  # 生成url
    url = 'http://' + user_in_city + '.lianjia.com/ershoufang/pg{}/'
    for url_next in range(1, int(user_in_nub)):
        yield url.format(url_next)


def get_allurl(generate_allurl):  # 分析url解析出每一页的详细url
    get_url = requests.get(generate_allurl, 'lxml')
    if get_url.status_code == 200:
        re_set = re.compile('<li.*?class="clear">.*?<a.*?class="img.*?".*?href="(.*?)"')
        re_get = re.findall(re_set, get_url.text)
        return re_get


def open_url(re_get):  # 分析详细url获取所需信息
    res = requests.get(re_get)
    if res.status_code == 200:
        info = {}
        soup = BeautifulSoup(res.text, 'lxml')
        info['标题'] = soup.select('.main')[0].text
        info['总价'] = soup.select('.total')[0].text + '万'
        info['每平方售价'] = soup.select('.unitPriceValue')[0].text
        info['参考总价'] = soup.select('.taxtext')[0].text
        info['建造时间'] = soup.select('.subInfo')[2].text
        info['小区名称'] = soup.select('.info')[0].text
        info['所在区域'] = soup.select('.info a')[0].text + ':' + soup.select('.info a')[1].text
        info['链家编号'] = str(re_get)[33:].rsplit('.html')[0]
        for i in soup.select('.base li'):
            i = str(i)
            if '</span>' in i or len(i) > 0:
                key, value = (i.split('</span>'))
                info[key[24:]] = value.rsplit('</li>')[0]
        for i in soup.select('.transaction li'):
            i = str(i)
            if '</span>' in i and len(i) > 0 and '抵押信息' not in i:
                key, value = (i.split('</span>'))
                info[key[24:]] = value.rsplit('</li>')[0]
        print(info)
        return info


def update_to_MongoDB(one_page):  # update储存到MongoDB
    if db[Mongo_TABLE].update({'链家编号': one_page['链家编号']}, {'$set': one_page}, True): #去重复
        print('储存MongoDB 成功!')
        return True
    return False


def pandas_to_xlsx(info):  # 储存到xlsx
    pd_look = pd.DataFrame(info)
    pd_look.to_excel('链家二手房.xlsx', sheet_name='链家二手房')


def writer_to_text(list):  # 储存到text
    with open('链家二手房.text', 'a', encoding='utf-8')as f:
        f.write(json.dumps(list, ensure_ascii=False) + '\n')
        f.close()


def main(url):

    writer_to_text(open_url(url))    #储存到text文件
    # update_to_MongoDB(list)   #储存到Mongodb


if __name__ == '__main__':
    user_in_city = input('输入爬取城市：')
    user_in_nub = input('输入爬取页数：')

    Mongo_Url = 'localhost'
    Mongo_DB = 'test'
    Mongo_TABLE = 'Lianjia' + '\n' + str('zs')
    client = pymongo.MongoClient(Mongo_Url)
    db = client[Mongo_DB]
    pool = Pool()
    for i in generate_allurl('2', 'zs'):
        pool.map(main, [url for url in get_allurl(i)])