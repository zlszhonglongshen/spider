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
import time
import json
import pymysql
from multiprocessing import Pool
from  urllib.parse import urlencode
from requests import RequestException
from urllib.request import urlopen
import chardet

# 需要指定编码集,不然会出异常!!!(很重要)
#db = pymysql.connect("localhost", "root", "", "mysql", use_unicode=True, charset='utf8mb4')
db = pymysql.connect(host='172.20.71.35', port=3306, user='root', passwd='root', db='mysql', charset='utf8mb4')

cursor = db.cursor()


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False

def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False
def format_str(content):
    content_str = ''
    for i in content:
        if is_chinese(i):
            content_str = content_str+i
    return content_str



#构造请求参数，模拟请求
def get_index_page(offset,keyword):
    query_data = {
        'aid': 24,
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis'
    }
    params = urlencode(query_data)

    #头条搜索api基础入口
    base_url = 'http://www.toutiao.com/api/search/content/'
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

#
# #解析数据，获取想要的数据
# def parse_index_page(html):
#     params = []
#     data = json.loads(html)
#     datas = data['data']
#     for item in datas:
#         if 'title' in item:  # 文章标题
#             title = item['title']
#         else:
#             title = None
#     # for item in datas:
#         if 'source' in item:  # 资源归属
#             source = item['source']
#         else:
#             source = None
#     # for item in datas:
#         if 'comment_count' in item:  # 评论数
#             countgood = item['comment_count']
#         else:
#             countgood = None
#     # for item in datas:
#         if 'abstract' in item:
#             abstract = item['abstract'] #文章摘要
#         else:
#             abstract = None
#     # for item in datas:
#         if 'datetime' in item:
#             datetime = item['datetime'] #文章发表时间
#         else:
#             datetime = None
#         params.append([title, source, countgood,abstract,datetime])
#     return params



#解析数据，获取想要的数据
def parse_index_page(html):
    try:
        params = []
        data = json.loads(html)
        datas = data['data']
        for item in datas:
            if 'title' in item:  # 文章标题
                title = item['title']
            if 'source' in item :  # 资源归属
                source = item['source']
            if 'article_url' in item:  # 资源链接
                url = item['article_url']
                content = parse_page_detail_toutiao(url)
                # if url[7:14]=='toutiao':
                #     content = parse_page_detail_toutiao(url)  # 解析文章内容
                # else:
                #     content = parse_page_detail_html(url)
            if 'share_url' in item:  # 分享链接,可作资源链接用
                share_url = item['share_url']
            if 'keyword' in item:  # 所属关键词
                keyword_ = item['keyword']
            if 'comment_count' in item:  # 评论数
                countgood = item['comment_count']
            if 'has_video' in item:  # 是否是视频链接
                has_video = item['has_video']
            if 'abstract' in item:
                abstract = item['abstract'] #文章摘要
            if 'datetime' in item:
                datetime = item['datetime'] #文章发表时间
                params.append([title, source, url, share_url, keyword_, countgood, has_video,abstract,datetime,content])
                # print(params)
        return params
    except:
        pass

def parse_page_detail_toutiao(url):
    '''
    :param html:
    :return: 解析文章具体内容
    '''
    html = get_page_detail(url) #获取html内容
    soup = bs(html,"lxml")
    try:
        content = soup.find("div", class_="article-content").get_text()
        return content
    except:
        pass

def parse_page_detail_html(url):
    '''
        :param html:
        :return: 解析文章具体内容
        '''
    pattern = re.compile('[\u4e00-\u9fa5]+')
    html = get_page_detail(url)  # 获取html内容
    soup = bs(html, "lxml")
    try:
        content = ''
        p_list = soup.find_all('p')
        for s in p_list:
            # content.append(re.sub("[A-Za-z0-9\!\%\[\]\,\。\\(\\)\\（\\）\'\'\,\，\ ]", "", s.string))
            # content.append(format_str(s.string))
            # content.append(''.join(re.findall(pattern,s.string))) #只保留中文
            content += s.get_text()+"\n"

        print(content)
        return content
    except:
        pass

def get_page_detail(url):
    '''
    解析URL
    :param url:
    :return:
    '''
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/52.0.2743.116 Safari/537.36 '
        }
        a = urlopen(url).read()
        b = chardet.detect(a)  #检测网页的标注是什么格式

        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"
        # print(b.get("encoding"))
        # if b.get("encoding")=="ascii":
        #     response.encoding = "gbk"
        # else:
        #     response.encoding = b.get("encoding")
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错', url)
        return None


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

    sql2 = """
    CREATE TABLE toutiao_python (
`title` varchar(50)  ,
`source` varchar(25)  ,
`url` varchar(500)  ,
`share_url` varchar(500)  ,
`keyword_` varchar(25)  ,
`countgood` varchar(25)  ,
`has_video` varchar(25)  ,
`abstract` varchar(500)  ,
`datetime` varchar(25),
`content` TEXT 
) character set utf8mb4
;
    """
    cursor.execute(sql2)
    print("***SQL执行完成***")


#储存至数据库
def save_data(params):
    try:
        sql = 'INSERT INTO toutiao_python VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'  #多个指标的1
        # sql = 'INSERT INTO toutiao_python VALUES (%s,%s,%s,%s,%s)'            #多个指标的2
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
CRAWLER_GO = 0
CRAWLER_END = 20
# 搜索关键字，可以改变

# 开启多线程
if __name__ == '__main__':
    mysql_()
    pool = Pool()
    group = [x * 20 for x in range(CRAWLER_GO, CRAWLER_END + 1)]
    pool.map(main, group)
    pool.close()
    pool.join()
