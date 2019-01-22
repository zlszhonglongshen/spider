# -*- coding: utf-8 -*-
"""
Created on 2019/1/21 22:22
@author: Johnson
Email:593956670@qq.com
@software: PyCharm
"""
import requests
import re
import urllib
import chardet
from bs4 import BeautifulSoup as bs
from bs4 import BeautifulSoup
import time
import json
import pymysql
from multiprocessing import Pool
from  urllib.parse import urlencode

# 需要指定编码集,不然会出异常!!!(很重要)
#db = pymysql.connect("localhost", "root", "", "mysql", use_unicode=True, charset='utf8mb4')
db = pymysql.connect(host='172.20.71.35', port=3306, user='root', passwd='root', db='mysql', charset='utf8mb4')

cursor = db.cursor()


#构造请求参数，模拟请求
def get_index_page(offset,keyword):
    query_data = {
        'offset':offset,
        'format':'json',
        'keyword':keyword,
        'autoload':'true',
        'count':20, #每次返回20篇文章
        'cur_tab':1
    }
    params = urlencode(query_data)

    #头条搜索api基础入口
    base_url = 'http://www.toutiao.com/search_content/'
    url = base_url+'?'+params
    print(url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # print(response.text)
            return response.text
        return None
    except Exception as e:
        print("页面索引出错,url")
        return None


#解析数据，获取想要的数据
def parse_index_page(html):
    params = []
    data = json.loads(html)
    datas = data['data']
    for item in datas:
        if 'title' in item:  # 文章标题
            title = item['title']
        else:
            title = None
    # for item in datas:
        if 'source' in item:  # 资源归属
            source = item['source']
        else:
            source = None
    # for item in datas:
        if 'comment_count' in item:  # 评论数
            countgood = item['comment_count']
        else:
            countgood = None
    # for item in datas:
        if 'abstract' in item:
            abstract = item['abstract'] #文章摘要
        else:
            abstract = None
    # for item in datas:
        if 'datetime' in item:
            datetime = item['datetime'] #文章发表时间
        else:
            datetime = None
        params.append([title, source, countgood,abstract,datetime])
    return params

#获取URL的详情
def get_page_detail(url):
    try:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        response = requests.get(url,headers = headers)
        if response.status_code==200:
            return response.text
        return None
    except Exception as e:
        print("请求详情页面失败",url)
        return None

#解析获取的html为json格式
def parse_page_detail(html,url):
    soup = BeautifulSoup(html,"lxml")
    title = soup.select('title')[0].get_text()



# #解析数据，获取想要的数据
# def parse_index_page(html):
#     params = []
#     data = json.loads(html)
#     datas = data['data']
#     for item in datas:
#         if 'title' in item:  # 文章标题
#             title = item['title']
#         if 'source' in item and item['source']!='综艺无限极':  # 资源归属
#             source = item['source']
#         if 'article_url' in item:  # 资源链接
#             url = item['article_url']
#         if 'share_url' in item:  # 分享链接,可作资源链接用
#             share_url = item['share_url']
#         if 'keyword' in item:  # 所属关键词
#             keyword_ = item['keyword']
#         if 'comment_count' in item:  # 评论数
#             countgood = item['comment_count']
#         if 'has_video' in item:  # 是否是视频链接
#             has_video = item['has_video']
#         if 'abstract' in item:
#             abstract = item['abstract'] #文章摘要
#         if 'datetime' in item:
#             datetime = item['datetime'] #文章发表时间
#             params.append([title, source, url, share_url, keyword_, countgood, has_video,abstract,datetime])
#     return params



'''
数据存储，这里将数据插入到mysql
'''

def mysql_():
    # 如果数据表已经存在使用 execute() 方法删除表。
    cursor.execute("DROP TABLE IF EXISTS toutiao_python")

    #创建数据表的SQL语句，后期需要修改
    sql = """
    CREATE TABLE toutiao_python (
    `title` varchar(50)  ,
    `source` varchar(25)  ,
    `countgood` varchar(25) ,
    `abstract` varchar(500)  ,
    `datetime` varchar(25)
    ) character set utf8mb4
    """
    cursor.execute(sql)
    print("***SQL执行完成***")


#储存至数据库
def save_data(params):
    try:
        # sql = 'INSERT INTO toutiao_python VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        sql = 'INSERT INTO toutiao_python VALUES (%s,%s,%s,%s,%s)'
        # 批量插入数据库
        cursor.executemany(sql, params)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()


def main(offset):
    html = get_index_page(offset,"无限极")
    params = parse_index_page(html)
    save_data(params)

# 指定搜索的参数offset范围为[CRAWLER_GO*20,(CRAWLER_END+1)*20]
CRAWLER_GO = 1
CRAWLER_END = 50
# 搜索关键字，可以改变

# 开启多线程
if __name__ == '__main__':
    mysql_()
    pool = Pool()
    group = [x * 20 for x in range(CRAWLER_GO, CRAWLER_END + 1)]
    pool.map(main, group)
    pool.close()
    pool.join()
