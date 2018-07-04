#coding:utf-8
import urllib.request
import re
import pymysql

# 爬取整个网页的方法
def open_url(url):
    req = urllib.request.Request(url)
    respond = urllib.request.urlopen(req)
    html = respond.read().decode('utf-8')
    return html


# 爬取每个页面中每一话漫画对应的链接
def get_url_list(url):
    html = open_url(url)
    p = re.compile(r'<a href="(.+)" title=".+ <br>.+?">')
    url_list = re.findall(p, html)
    return url_list


# 自动进入每一话漫画对应的链接中爬取每一张图片对应的链接并插入到mysql数据库
def get_img(url):
    # 获取每个页面中每一话漫画对应的链接
    url_list = get_url_list(url)
    # 连接mysql数据库
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='test')
    # 创建游标
    c = conn.cursor()
    try:
        # 创建一张数据库表
        c.execute('create table cartoon(name varchar(30) ,img varchar(100))')
    except:
        # count用来计算每一张网页有多少行数据被插入
        count = 0
        for each_url in url_list:
            html = open_url(each_url)
            p1 = re.compile(r'<img src="(.+)" alt=".+?>')
            p2 = re.compile(r'<h1>(.+)</h1>')
            img_list = re.findall(p1, html)
            title = re.findall(p2, html)
            for each_img in img_list:
                c.execute('insert into cartoon values(%s,%s)', [title[0], each_img])
                count += c.rowcount
        print('有%d行数据被插入' % count)

    finally:
        # 提交数据，这一步很重要哦！
        conn.commit()
        # 以下两步把游标与数据库连接都关闭，这也是必须的！
        c.close()
        conn.close()


num = int(input('前几页：'))
for i in range(num):
    url = 'http://www.ishuhui.com/page/' + str(i + 1)
    get_img(url)