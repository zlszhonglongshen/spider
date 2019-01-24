# -*- coding: utf-8 -*-
"""
Created on 2019-01-24 16:50
@author: Johnson
Email:593956670@qq.com
@software: PyCharm
"""
import requests
import json
from bs4 import BeautifulSoup
import re

#获得每页新闻标题和新闻地址
def getPageInfo(url,page):
    newurl=url + str(page)
    res = requests.get(newurl)
    jd = json.loads(res.text)
    list1 = jd['data']['list']
    it = iter(list1)
    for one in it:
        print("\t新闻标题="+one['title']+"\t"+"新闻地址="+one['url'])


#获得各个种类的新闻信息
def getInfo(classInfo):
    print("种类是："+classInfo)
    #当种类为 “推荐” 的时候他的url和其他的种类URL不一样，所以单独处理
    if classInfo == '推荐':
        url = 'http://jian.news.baidu.com/ajax/list?type=chosen/推荐&pn='
        getPageInfo(url,1)
    else:
        url = 'http://jian.news.baidu.com/ajax/list?type=info/{}&pn='.format(classInfo)
        #print(url)
        #这里取的是分页信息 我只取了前4页 取分页信息在这里修改
        for page in range(1,2):
            getPageInfo(url,page)


#获得新闻的种类
def getClassInfo():
    list2 = []
    res = requests.get('http://jian.news.baidu.com/')
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    data = soup.select('script')[2].text
    #下面用了正则表达式来替换，为了得到我们想要的数据
    sea = re.sub('\s',"",data)
    sea = sea.rstrip("window.menulist=menulist;")
    ss = re.sub('varmenulist=\[\];',"",sea)
    #print(ss)
    ss = re.sub('menulist.push\(',"",ss)
    ss = re.sub('\);',";",ss)
    ss = re.sub('\)',"",ss)
    ss = re.sub('\'',"\"",ss)
    list1 = ss.split(';')
    #print(list1)
    it = iter(list1)
    for one in it:
        #print(one)
        jd = json.loads(one)
        #print(type(jd))
        #print(jd['topic'])
        list2.append(jd['topic'])

    return list2

listt = getClassInfo()
it = iter(listt)
for one in it:
    getInfo(one)
