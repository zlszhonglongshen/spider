#coding:utf-8
import urllib2
from bs4 import BeautifulSoup
import csv
import re
import sys
reload(sys)
sy.setdefaultencoding('utf-8')
for k in range(0,100):
    req = urllib2.Request('http://tieba.baidu.com/f?kw=李毅&ie=utf-8&pn=' + str(k * 50))
    csvfile = file('e:/tiezi.csv', 'ab+')
    writer = csv.writer(csvfile)
    response = urllib2.urlopen(req)
    the_page = response.read()
    soup = BeautifulSoup(the_page,"lxml")
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    for tag in soup.find_all(name="a", attrs={"class": re.compile("j_th_tit")}):
        list1.append("http://tieba.baidu.com" + tag['href'])
        list2.append(tag.string)
    for tag in soup.find_all(name="span", attrs={"class": re.compile("threadlist_rep_num.*")}):
        list3.append(tag.string)
    for tag in soup.find_all(name="span", attrs={"class": re.compile("tb_icon_author$")}):
        list4.append(tag['title'])
    for tag in soup.find_all(name="span", attrs={"class": re.compile("tb_icon_author_rely")}):
        list5.append(tag['title'])
    data = []
    for i in range(0, len(soup.find_all(name="a", attrs={"class": re.compile("j_th_tit")}))):
        data.append((list1[i], list2[i], list3[i], list4[i]))
    # writer.writerows(data)
    # csvfile.close()
    print(data)
    print "第" + str(k) + "页完成"
