#coding:utf-8
import urllib
from bs4 import BeautifulSoup
import csv
import codecs

c = open("test.csv", "wb")  # 创建文件
c.write(codecs.BOM_UTF8)  # 防止乱码
writer = csv.writer(c)  # 写入对象
writer.writerow(['产品', '价格', '单位', '批发地', '时间'])

i = 1
while i <= 4:
    print("爬取第" + str(i) + "页")
    url = "http://www.gznw.gov.cn/priceInfo/getPriceInfoByAreaId.jx?areaid=22572&page=" + str(i)
    content = urllib.urlopen(url).read()
    soup = BeautifulSoup(content, "html.parser")
    print
    soup.title.get_text()
    tt = soup.find_all("tr", class_="odd gradeX")
    for t in tt:
        content = t.get_text()
        num = content.splitlines()
        print(num[0], num[1], num[2], num[3], num[4], num[5])
        # 写入文件
        templist = []
        num[1] = num[1].encode('utf-8')
        num[2] = num[2].encode('utf-8')
        num[3] = num[3].encode('utf-8')
        num[4] = num[4].encode('utf-8')
        num[5] = num[5].encode('utf-8')
        templist.append(num[1])
        templist.append(num[2])
        templist.append(num[3])
        templist.append(num[4])
        templist.append(num[5])
        # print templist
        writer.writerow(templist)
    i = i + 1

c.close()