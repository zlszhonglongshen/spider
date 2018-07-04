# -*- coding: utf-8 -*-
import os
import time
import urllib2
import threading
import re
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def getListHtml(url, header1, header2):
  print ("\n" + '------------URL:' + url + '-----------------------' + "\n")
  req1 = urllib2.Request(url, headers = header1)
  try:
    con1 = urllib2.urlopen(req1, data=None, timeout=20)
    listhtml = con1.read()
    con1.close()
    soup = BeautifulSoup(listhtml)
    soup.prettify()
    one = soup.find('ul', {'class', 'agent-lst'})
    if one:
      two = one.find_all('li')
      if two:
        for three in two:
          four = three.find('div', {'class', 'pic-panel'}).find('a').get('href'); #作者详情链接
          five = three.find('div', {'class', 'pic-panel'}).find('img').get('src'); #作者照片
          six = three.find('div', {'class', 'agent-name'}).find('a').get_text(); #经纪人姓名
          sevenbug = three.find('div', {'class', 'agent-name'}).find('span')
          seven = ''
          if sevenbug:
              seven = sevenbug.get_text(); #经纪人Title
          eight = three.find('div', {'class', 'achievement'}).get_text()
          mode = re.compile(r'\d+')
          nine = mode.findall(str(eight)) #历史成交 30 天看房记录
          ten = three.find('span', {'class', 'num'}).get_text()
          eleven = three.find('div', {'class', 'comment-num'}).get_text();
          onethree = '广州'; #板块
          oneone = three.find('div', {'class', 'main-plate'}).find_all('a');
          if oneone:
              for onetwo in oneone:
                  onethree = onethree + '||' + onetwo.get_text()
          twoone = three.find('div', {'class', 'col-3'}).find('h2').get_text() # 联系方式
          uidmode = re.compile(r'\d+')
          uid = uidmode.findall(four) #uid
          # print seven + '-' + six + '-' + str(nine[0]) + '|' + str(nine['1'])
          content = str(uid[0]) + '=' + onethree + '=' + twoone + '=' + seven + '=' + six + '=' + str(nine[0]) + '=' + str(nine[2]) + '=' + str(ten) + '=' + eleven
# for nine in eight:
# print nine
          filename = "guangzhou_lianjia_agent.txt"
          f = open(filename, "a")
          f.write(content + "\n")
          f.close
          print content + "\n"
# exit()
# getContentOne(html, header, header2)
        except Exception, e:
        print "List Page Error ---------" + str(e)
  filename = "lianjia_agent_log.txt"
  f = open(filename, "a")
  f.write(url + "\n")
  f.close
header1 = {'Host': 'gz.lianjia.com',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding': 'deflate',
'Connection': 'keep-alive'}
header2 = {'Host': 'dianpu.lianjia.com',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding': 'deflate',
'Connection': 'keep-alive'}
url = raw_input("Url: ")
page = raw_input("Page: ")
for i in xrange (1,int(page)+1):
    getListHtml(url + 'pg' + str(i), header1, header2)