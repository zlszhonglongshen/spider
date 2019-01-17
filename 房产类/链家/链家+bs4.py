# coding:utf-8
import urllib2
from bs4 import BeautifulSoup
import csv
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# 根据网页数设置范围
for k in range(1, 6):
    # 根据网址获取网页
    req = urllib2.Request('http://bj.fang.lianjia.com/loupan/pg' + str(k))

    # 建立csv存储文件，wb写 a+追加模式
csvfile = file('e:/lianjia.csv', 'ab+')
writer = csv.writer(csvfile)
# 读取网页
response = urllib2.urlopen(req)
the_page = response.read()

# 解析网页
soup = BeautifulSoup(the_page, "lxml")
list0 = []
list1 = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []
# 提取楼盘名称字段
for tag in soup.find_all(name="div", attrs={"class": re.compile("col-1")}):
    ta1 = tag.find(name="a", attrs={"target": re.compile("_blank")})
    # 添加城市字段
    list0.append('长沙')
    list1.append(ta1.string)

    # 提取建筑面积字段
    ta2 = tag.find(name="div", attrs={"class": re.compile("area")})
    t2 = ta2.find(name="span")
    if t2 != None:
        list2.append(t2.string)
    else:
        list2.append(0)
# 提取在售状态字段
    ta3 = tag.find(name="span", attrs={"class": re.compile("onsold")})
    list3.append(ta3.string)
# 提取住宅类型字段

    ta4 = tag.find(name="span", attrs={"class": re.compile("live")})
    list4.append(ta4.string)

# 提取每平米均价字段
for tag in soup.find_all(name="div", attrs={"class": re.compile("col-2")}):
    ta5 = tag.find(name="span", attrs={"class": re.compile("num")})
    if ta5 != None:
        list5.append(ta5.string)
    else:
        list5.append(0)
        # 提取总价字段
    ta6 = tag.find(name="div", attrs={"class": re.compile("sum-num")})
    if ta6 != None:
        t6 = ta6.find(name="span")
        list6.append(t6.string)
    else:
        list6.append(0)
        # 将提取的数据合并
data = []
for i in range(0, len(soup.find_all(name="div", attrs={"class": re.compile("col-1")}))):
    data.append((list0[i], list1[i], list2[i], list3[i], list4[i], list5[i], list6[i]))
    # 将合并的数据存入csv
# writer.writerows(data)
# csvfile.close()
print (data)
print ("第" + str(k) + "页完成")
