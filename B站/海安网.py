import requests, re, sys
from bs4 import BeautifulSoup
import pyodbc

pages = set()

conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=WXS-PC;DATABASE=Test;UID=sa')
cursor = conn.cursor()


# 递归爬取整个网站，并将链接存入集合
def getLinks(pageUrl):
    global pages
    r = requests.get(pageUrl, timeout=30)
    demo = r.text
    bsObj = BeautifulSoup(demo, 'html.parser')
    # 去除外链
    for link in bsObj.findAll('a', href=re.compile("(www.haianw.com)+")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                findPhone(newPage)
                pages.add(newPage)
                getLinks(newPage)


# 将当前url中的手机号存入字典
def findPhone(url):
    numbers = {}
    r = requests.get(url, timeout=30)
    data = r.text
    # 电话号码和手机号码正则表达式
    phone_list = re.findall(r"\d{3}-\d{8}|\d{4}-\d{7}|1[34578]\d{9}", data)
    phone_list = list(set(phone_list))
    for phone in phone_list:
        numbers[phone] = url
    writePhone(numbers)


def writePhone(numbers):
    global cursor
    global conn
    for k, v in numbers.items():
        temp = "insert into Numbers (link,number) values ('{}','{}')".format(v, k)
        cursor.execute(temp)
        conn.commit()


if __name__ == '__main__':

    # 设置递归深度为一百万，防止爬虫崩溃
    sys.setrecursionlimit(1000000)
    print("开始爬取全站链接...")
    try:
        getLinks('http://www.haianw.com')
    except Exception:
        print('爬虫发生崩溃错误，已停止爬取...')

