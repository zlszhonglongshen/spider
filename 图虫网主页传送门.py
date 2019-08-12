#!/usr/bin/python_人脸属性相关
# coding:utf-8

import urllib2, time, uuid, urllib, os, sys, re
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')


# 获得网页内容
def getHtml(url):
    try:
        print url
        html = urllib2.urlopen(url).read()  # .decode('utf-8')#解码为utf-8
    except:
        return
    return html


# 获取主页下子页面地址	url,以及作者名字
def getUrls(html):
    if not html:
        print 'nothing can be found'
        return
    print 'start find url'
    mylist = []
    soup = BeautifulSoup(html, 'lxml')
    try:
        items = soup.find_all("div", {"class": "post-collage"})
        print len(items)

        for item in items:
            alist = {}

            if item.find('a', {"data-location": "content"}):
                newurl = item.find('a', {"data-location": "content"}).get('href')
                alist['url'] = newurl

            if item.find('a', {"class": "site-anchor"}):
                author = item.find('a', {"class": "site-anchor"}).text
                alist['author'] = author

            mylist.append(alist)
    except:
        return None
    return mylist


# 获取图片rul地址
def getImagUrl(html):
    if not html:
        print 'nothing can be found'
        return
    # print 'start find imgurl'
    ImagUrlList = []
    soup = BeautifulSoup(html, 'lxml')
    # print 'start find imgurl'
    items = soup.find("div", {"class": "figures-wrapper"}).find_all('img',
                                                                    {'class': 'img-responsive copyright-contextmenu'})
    for item in items:
        imgurl = item.get('src')
        ImagUrlList.append(imgurl)
    return ImagUrlList


# 下载图片到本地
def download(author, ImagUrlList, typename, pageNo):
    # 定义文件夹的名字
    x = time.localtime(time.time())
    foldername = str(x.__getattribute__("tm_year")) + "-" + str(x.__getattribute__("tm_mon")) + "-" + str(
        x.__getattribute__("tm_mday"))
    download_img = None
    for imgurl in ImagUrlList:
        picpath = 'TuChong/%s/%s/%s/%s' % (foldername, typename, str(pageNo), author)
        filename = str(uuid.uuid1())
        if not os.path.exists(picpath):
            os.makedirs(picpath)
        target = picpath + "/%s.jpg" % filename
        print "The photos location is:" + target
        download_img = urllib.urlretrieve(imgurl, target)  # 将图片下载到指定路径中
        time.sleep(1)
        print(imgurl)
    return download_img


# 退出程序
def myquit():
    print "Bye Bye!"
    exit(0)


# 输入参数
def control_func():
    print '''
			*****************************************
			**    Welcome to Spider of TUCHONG     **
			**      Created on 2017-3-15           **
			**      @author: Jimy                  **
			*****************************************'''

    print '''
			可选择类型如下：
			***********************************************
			**  1:'人像',2:'风光',3:'城市',4:'纪实',     **
			**  5:'街拍',6:'旅行',7:'美女',8:'人文',     **
			**  9:'建筑',10:'自然',11:'夜景',12:'静物'   **
			**  13:'少女',14:'花卉',15:'光影',16:'动物'  **
			**  17:'植物',18:'儿童',19:'生活',20:'私房'  **
			***********************************************'''
    typenum = raw_input("Input the page number you want to choose (1-20),please input 'quit' if you want to quit\
						 请输入要选择的类型前面的额数字，范围为（1-20），如果退出，请输入Q>>>\n")
    while not typenum.isdigit() or int(typenum) > 20 or int(typenum) < 1:
        if typenum == 'Q':
            myquit()
        print "Param is invalid , please try again."
        typenum = raw_input("Input the page number you want to scratch >")

    pageNo = raw_input("Input the page number you want to scratch (1-50),please input 'quit' if you want to quit\
						请输入要爬取的页面，范围为（1-50），如果退出，请输入Q>>>\n")
    while not pageNo.isdigit() or int(pageNo) > 50 or int(typenum) < 1:
        if pageNo == 'Q':
            myquit()
        print "Param is invalid , please try again."
        pageNo = raw_input("Input the page number you want to scratch >")
    return pageNo, typenum


if __name__ == '__main__':
    typeOfmydownload = ['人像', '风光', '城市', '纪实', '街拍', '旅行', '美女', '人文', '建筑', '自然', '夜景', '静物', '少女', '花卉', '光影', '动物',
                        '植物', '儿童', '生活', '私房']
    pageNo, typenum = control_func()
    # 针对图虫人像模块来爬取
    targeturl = "http://tuchong.com/tags/" + typeOfmydownload[int(typenum) - 1] + "/?page=" + str(pageNo)
    html = getHtml(targeturl)
    urllist = getUrls(html)
    print len(urllist)
    for imgurl in urllist:
        imghtml = getHtml(imgurl['url'])
        imglist = getImagUrl(imghtml)
        print len(imglist)
        download(imgurl['author'], imglist, typeOfmydownload[int(typenum) - 1], pageNo)