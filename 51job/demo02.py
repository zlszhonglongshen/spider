# -*- coding:utf-8 -*-
import requests
import re, pymysql
import time


db = pymysql.connect(host='172.20.71.35', port=3306, user='root', passwd='root', db='mysql', charset='utf8mb4') #连接数据库，设置数据库参数
print('连接成功')
cursor = db.cursor()
cursor.execute('DROP TABLE IF EXISTS JOBS')
SQL = '''CREATE TABLE JOBS( 
    POSITION TEXT(1000) NOT NULL,
    COMPANY TEXT(1000),
    ADDRESS TEXT(1000),
    SALARY TEXT(1000),
    DATE TEXT(1000))'''
cursor.execute(SQL)


def get_content(page):
    url = 'http://search.51job.com/list/000000,000000,0000,00,9,99,%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590,2,' + str(
        page) + '.html'
    time.sleep(3)
    html = requests.get(url)
    s = requests.session()
    s.keep_alive = False
    html.encoding = 'gbk'
    return html


def get(html):
    reg = re.compile(
        r'class="t1 ">.*? <a target="_blank" title="(.*?)".*? <span class="t2"><a target="_blank" title="(.*?)".*?<span class="t3">(.*?)</span>.*?<span class="t4">(.*?)</span>.*? <span class="t5">(.*?)</span>',
        re.S)  # 匹配换行符
    items = re.findall(reg, html.text)
    return items


def savetosql(items):
    print('正在连接到服务器')
    # db = pymysql.connect('localhost', 'root', '', 'mysql', charset="utf8")
    db = pymysql.connect(host='172.20.71.35', port=3306, user='root', passwd='root', db='mysql', charset='utf8mb4')
    print('连接成功')
    cursor = db.cursor()
    print('创建成功')
    for item in items:
        sql = "insert into JOBS values('%s','%s','%s','%s','%s')" % (item[0], item[1], item[2], item[3], item[4])
        print(item[1])
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print('插入失败')
            db.rollback()


for page in range(1, 2000):
    print('正在爬取第{}页'.format(page))
    savetosql(get(get_content(page)))