#-*- coding: utf-8 -*-

import re
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import requests
from multiprocessing import Pool
import time

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

# 获取页面信息
def get_page_index(page_num):
    url = 'https://bookset.me/page/'+ str(page_num) + '?rating=douban'
    print(url)
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引出错')
        return None

# 获取当页所有书的URL
def parse_page_index(html):
    pattern = re.compile(r'class="thumb-img focus"> <a href="(.*?)" title="(.*?)">', re.S)
    items = re.findall(pattern, html)
    print(items)
    print(type(items))
    for item in items:
        yield {
            'href': item[0],
            'title': item[1]
        }

# 获取详情页信息
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
def parse_page_detail(html, title):
    soup = BeautifulSoup(html, 'lxml')
    time.sleep(10)
    #匹配包含书链接的标签，而且取最后一个下载链接，以mobi格式下载为主
    book_link_tag = soup.find_all("a", class_ = "mbm-book-download-links-link")[-1]
    book_link_pattern = re.compile(r'href="(.*?)"', re.S)
    # 书下载链接直接用正则表达式死活匹配匹配不出来，故作了两次转换
    book_link = re.search(book_link_pattern, str(book_link_tag)).group(1)
    editors_tag = soup.select(".mbm-book-details-editors-data")
    for editor in editors_tag:
        editors = editor.get_text().replace(' ','-')
    # 书的名字格式
    book_name = editors + '-' + title
    # 获取文件格式
    book_format = book_link[-4:]
    down_load_book(book_link, book_name, book_format)
    time.sleep(5)
    print(book_name)
    print(book_link)
    print(book_format)

# 下载书文件
def down_load_book(book_link, book_name, book_format):
    print('正在下载:', book_link)
    try:
        response = requests.get(book_link, headers = headers)
        if response.status_code == 200:
            save_bookes(response.content, book_name, book_format)
        return None
    except RequestException:
        print('请求文件出错', book_link)
        return None

# 存储书文件
def save_bookes(content, book_name, book_format):
    # 保存到当前目录下
    file_path = '{0}.{1}'.format(book_name, book_format)
    with open(file_path, 'wb') as f:
        f.write(content)
        f.close()

def main(page_num):
    html = get_page_index(page_num)
    for i in parse_page_index(html):
        content = get_page_detail(i['href'])
        parse_page_detail(content, i['title'])
        # 为了调试方便，只抓取每一页第一本，加了break跳出当页所有书链接的循环#############
        # break

if __name__ == '__main__':
    # 利用多线程，同时请求前5页下载
    groups = [x for x in range(1, 6)]
    pool = Pool()
    pool.map(main, groups)

# 作者：nobodyyang
# 链接：https://www.jianshu.com/p/7173b9d48f2c
# 來源：简书
# 简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。