# -*- coding: utf-8 -*-
"""
Created on 2019-01-27 15:01
@author: Johnson
Email:593956670@qq.com
@software: PyCharm
"""
from pyquery import PyQuery as pq
import requests
import codecs
import json
import pymysql
import sys
import time
import re

s = requests.Session()
s.headers.update({'referer': "http://news.baidu.com"})
try:
    conn=pymysql.connect(host='172.20.71.35', port=3306, user='root', passwd='root', db='mysql', charset='utf8mb4')
    # conn.set_character_set('utf8')
    cur=conn.cursor()
    cur.execute("SET NAMES 'utf8'")
    cur.execute("DROP TABLE IF EXISTS records")
    cur.execute("create table records(id int not null auto_increment primary key,keyword varchar(1023), title varchar(1023), source varchar(1023),time varchar(1023), url varchar(1023))")
    # cur.close()
    # conn.close()
except pymysql.Error as e:
     print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
     exit(0)


def indexPage(url,headers,keyword):
    r_page=s.get(url, headers=headers)
    page0=pq(r_page.text)
    num=len(page0('.norsSuggest'))
    while num!=0:
        print("sleep for 20s, zzZZ")
        # time.sleep(20)
        time.sleep(5)
        r_page=s.get(url, headers=headers)
        page0=pq(r_page.text)
        num=len(page0('.norsSuggest'))
    r_page.encoding = 'utf-8'
    page=pq(r_page.text)
    items=page(".result.title")
    for i in range(20):
        try:
            item=items.eq(i)
            # print(item)
            url=item('h3>a').attr('href')
            url=url.replace("'", "''")
            title=item('h3>a').text()
            title=title.replace("'", "''")
            time=item('.c-title-author').text()
            regex = "[\u4E00-\u9FA5]+"
            source = re.match(regex, time[0:7]).group(0)
            if time[-2:]==">>":
                time=time[:time.rindex(' ')]
            time=time[-17 : ]
            time=time.replace("'", "''").replace('年', '-').replace('月', '-').replace('日', '')
            sql="insert into records(keyword,title,source,time, url) values('%s','%s','%s', '%s', '%s')" %(keyword,source,title, time, url)
            try:
                cur.execute(sql)
                conn.commit()
            except Exception as e:
                print(e)
        except:
            pass


headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17"}

for n in range(0,501,20):
    for i in ["无限极","直销 无限极", "保健品" ,"权健"]:
        print ("n=", n)
        url = 'http://news.baidu.com/ns?word={}&pn='.format(i) + str(n) + '&cl=2&ct=0&tn=newstitle&rn=20&ie=utf-8&bt=0&et=0&clk=sortbytime'
        print(url)
        indexPage(url,headers,i)
        time.sleep(10)
cur.close()
conn.close()
