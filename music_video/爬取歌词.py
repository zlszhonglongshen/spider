#coding:utf-8
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import  numpy
import csv

starturl="http://www.cnlyric.com/geshou/1927.html" # 凤凰传奇歌词地址第一页

#找出下一页的链接

# 找出下一页的链接
def findnextlinks(starturl,nextlinks):
    """ 该函数用于从starturl页面开始，递归找出所有“下一页”的链接地址
    要求nextlinks为一个空的列表"""
    try:
        html=urlopen(starturl)
        bsobj=BeautifulSoup(html,"lxml")
        nextpagelink=bsobj.find("div",{"class":"PageList"}).input.\
        previous_sibling.previous_sibling.attrs["href"]
        nextlink="http://www.cnlyric.com/geshou/"+nextpagelink
        nextlinks.append(nextlink)
        findnextlinks(nextlink,nextlinks)
    except:
        print("\n所有“下一页”的链接寻找完毕")
    return nextlinks

nextlinks=[]
nextlinks=findnextlinks(starturl,nextlinks) # 所有“下一页”的链接列表


#找出存放歌词的链接列表
def findlrclinks(urllists):
    """ 该函数用于找出列表urllists中的链接页面上存放歌词的链接 """
    Sites=[]
    for urllist in urllists:
        html=urlopen(urllist)
        bsobj=BeautifulSoup(html,"lxml")
        for link in bsobj.findAll(href=re.compile("^(../LrcXML/)")):
            site="http://www.cnlyric.com"+link.attrs["href"].lstrip("..")
            Sites.append(site)
    return Sites

nextlinks.insert(0,starturl) # 将开始页面也加入链接列表中
Sites=findlrclinks(nextlinks) # 找出所有存放歌词的链接
print("\n所有曲目歌词所在的xml文件链接寻找完毕")

def getlrc(lrclink):
    """ 该函数用于找出歌词链接lrclink中的歌词，并以列表形式保存 """
    LRC=[]
    html=urlopen(lrclink)
    bsobj=BeautifulSoup(html,"lxml")
    lrcpre=bsobj.findAll("lrc")
    for lrclabel in lrcpre:
        lrc=lrclabel.get_text()
        LRC.append(lrc)
    return LRC

csvfile=open("凤凰传奇歌词集.csv","w+") # 创建csv文件用于保存数据
try:
    writer=csv.writer(csvfile)
    rowindex=1
    for lrcurl in Sites:
        LRC=getlrc(lrcurl)
        LRC.insert(0,str(rowindex).zfill(3))
        writer.writerow(LRC) # 将每首哥编号并将歌词写入从中文件中
        rowindex+=1
finally:
    csvfile.close() # 关闭csv文件