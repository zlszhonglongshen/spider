# -*- coding: utf-8 -*-
"""
Created on 2019/1/19 14:04
@Author: Johnson
@Email:593956670@qq.com
@File: 京东图书图片.py
"""
import re
import urllib.request
import urllib.error
import urllib.parse

sum = 0


def craw(url, page):
    htmll = urllib.request.urlopen(url).read()
    htmll = str(htmll)
    pat1 = r'<div id="plist".+? <div class="page clearfix">'
    result1 = re.compile(pat1).findall(htmll)
    result1 = result1[0]
    pat2 = r'<img width="200" height="200" data-img="1" src="//(.+?\.jpg)">|<img width="200" height="200" data-img="1" data-lazy-img="//(.+?\.jpg)">'
    imagelist = re.compile(pat2).findall(result1)
    x = 1
    global sum
    for imageurl in imagelist:
        imagename = 'h:/books/' + str(page) + ':' + str(x) + '.jpg'
        if imageurl[0] != '':
            imageurl = 'http://' + imageurl[0]
        else:
            imageurl = 'http://' + imageurl[1]
        print('开始爬取第%d页第%d张图片' % (page, x))

        try:
            urllib.request.urlretrieve(imageurl, filename=imagename)
        except urllib.error.URLError as e:
            if hasattr(e, 'code') or hasattr(e, 'reason'):
                x += 1
        print('成功保存第%d页第%d张图片' % (page, x))
        x += 1
        sum += 1


for i in range(1, 251):
    url = 'https://list.jd.com/list.html?cat=1713,3287,3797&page=' + str(i)
    craw(url, i)
print('爬取图片结束，成功保存%d张图' % sum)