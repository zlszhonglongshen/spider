# -*- coding: utf-8 -*-
"""
Created on 2019-01-24 17:35
@author: Johnson
Email:593956670@qq.com
@software: PyCharm
"""

'''
百度百家新闻收集
'''
import re
import bs4
import urllib.request
import pymysql

# 配置参数
maxcount = 1000  # 数据数量
home = 'http://baijia.baidu.com/'  # 起始位置
# 数据库连接参数
db_config = {
    'host': 'localhost',
    'port': '3310',
    'username': 'woider',
    'password': '3243',
    'database': 'python',
    'charset': 'utf8'
}

url_set = set()  # url集合
url_old = set()  # 过期url

# 获取首页链接
html = urllib.request.urlopen(home).read().decode('utf8')
soup = bs4.BeautifulSoup(html, 'html.parser')
pattern = 'http://\w+\.baijia\.baidu\.com/article/\w+'
links = soup.find_all('a', href=re.compile(pattern))
for link in links:
    url_set.add(link['href'])


# 文章类定义
class Article(object):
    def __init__(self):
        self.url = None
        self.title = None
        self.author = None
        self.date = None
        self.about = None
        self.content = None


# 连接数据库
# connect = pymysql.Connect(
#     host=db_config['host'],
#     port=int(db_config['port']),
#     user=db_config['username'],
#     passwd=db_config['password'],
#     db=db_config['database'],
#     charset=db_config['charset']
# )

connect = pymysql.connect(host='172.20.71.35', port=3306, user='root', passwd='root', db='mysql', charset='utf8mb4')
cursor = connect.cursor()

#处理URL信息
count = 0
while len(url_set)!=0:
    try:
        #获取链接
        url = url_set.pop()
        url_old.add(url)
        # 获取代码
        html = urllib.request.urlopen(url).read().decode('utf8')

        # DOM解析
        soup = bs4.BeautifulSoup(html, 'html.parser')
        pattern = 'http://\w+\.baijia\.baidu\.com/article/\w+'  # 链接匹配规则
        links = soup.find_all('a', href=re.compile(pattern))

        # 获取URL
        for link in links:
            if link['href'] not in url_old:
                url_set.add(link['href'])

        # 数据防重
        sql = "SELECT id FROM news WHERE url = '%s' "
        data = (url,)
        cursor.execute(sql % data)
        if cursor.rowcount != 0:
            raise Exception('Data Repeat Exception: ' + url)

        #获取信息
        article = Article()
        article.url = url #url信息
        page = soup.find('div',{'id':'page'})
        article.title = page.find('h1').get_text() #标题信息
        info = page.find('div', {'class': 'article-info'})
        article.author = info.find('a', {'class': 'name'}).get_text()  # 作者信息
        article.date = info.find('span', {'class': 'time'}).get_text()  # 日期信息
        article.about = page.find('blockquote').get_text()
        pnode = page.find('div', {'class': 'article-detail'}).find_all('p')
        article.content = ''
        for node in pnode:  # 获取文章段落
            article.content += node.get_text() + '\n'  # 追加段落信息

        # 存储数据
        sql = "INSERT INTO news( url, title, author, date, about, content ) "
        sql = sql + " VALUES ('%s', '%s', '%s', '%s', '%s', '%s') "
        data = (article.url, article.title, article.author, article.date, article.about, article.content)
        cursor.execute(sql % data)
        connect.commit()

    except Exception as e:
        print(e)
        continue
    else:
        print(article.title)
        count += 1
    finally:
        # 判断数据是否收集完成
        if count == maxcount:
            break

# 关闭数据库连接
cursor.close()
connect.close()