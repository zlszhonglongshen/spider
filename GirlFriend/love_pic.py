# -*- coding: utf-8 -*-
"""
Created on 2019/1/19 14:52
@Author: Johnson
@Email:593956670@qq.com
@File: love_pic.py
"""
#urllib模块提供了读取Web页面数据的接口
import urllib.request
import time
#re模块主要包含了正则表达式
import re


headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept - Encoding':'gzip, deflate',
               'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection':'Keep-Alive',
               'Host':'zhannei.baidu.com',
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
#定义一个getHtml()函数
def getHtml(url):
    req = urllib.request.Request(url=url,headers=headers)
    page = urllib.request.urlopen(req)  #urllib.request.urlopen()方法用于打开一个URL地址
    html = page.read() #read()方法用于读取URL上的数据
    return html

def getImg(html,x):
    reg = r'src="(.+?\.jpg)" pic_ext'    #正则表达式，得到图片地址
    imgre = re.compile(reg)     #re.compile() 可以把正则表达式编译成一个正则表达式对象.
    html = html.decode('utf-8') #python3
    imglist = re.findall(imgre,html)      #re.findall() 方法读取html 中包含 imgre（正则表达式）的数据
    #把筛选的图片地址通过for循环遍历并保存到本地
    #核心是urllib.request.urlretrieve()方法,直接将远程数据下载到本地，图片通过x依次递增命名
    for imgurl in imglist:
        urllib.request.urlretrieve(imgurl,'e:\LovePic\%s.jpg' % x)
        x += 1
    return x

x = 1
url = "https://tieba.baidu.com/p/3108805355?pn="
for k in range(1,22):
    try:
        ul = url+str(k)
        print(ul)
        html = getHtml(ul)
        time.sleep(5)
        x = getImg(html,x)
    except:
        pass