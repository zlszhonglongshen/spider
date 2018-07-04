#coding:utf-8
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import numpy
import csv

def getdatawithtablehead(url):
    """ 该函数用于获取带表头的数据 """
    html=urlopen(url)
    bsobj=BeautifulSoup(html,"lxml") # 获取BeautifulSoup对象

    tablelist=bsobj.findAll("tr") # 获取所有的表格

    Dataset=[]
    tablehead=tablelist[0].get_text().strip("\n").split("\n\n")
    Dataset.append(tablehead) # 获取表头

    for datalist in tablelist[1:]:
        data=datalist.get_text().replace(" ","").replace("\n\r","").\
        strip("\n").split("\n")
        Dataset.append(data) # 获取当月每一天的数据

    return Dataset

def getdata(url):
    """ 该函数用于获取不带表头的数据 """
    html=urlopen(url)
    bsobj=BeautifulSoup(html,"lxml")

    tablelist=bsobj.findAll("tr")

    dataset=[]
    for datalist in tablelist[1:]:
        data=datalist.get_text().replace(" ","").replace("\n\r","").\
        strip("\n").split("\n")
        dataset.append(data)

    return dataset

# 兰州空气质量指数(AQI)-PM2.5查询地址：
starturl="http://www.tianqihoubao.com/aqi/lanzhou.html"
html=urlopen(starturl)
bsobj=BeautifulSoup(html,"lxml") # 获取BeautifulSoup对象

# 找到所有存放月度数据的网页链接，并以列表的形式按月份先后顺序保存这些链接
Sites=[]
for link in bsobj.findAll(href=re.compile("^(/aqi/lanzhou-)")):
    site="http://www.tianqihoubao.com"+link.attrs['href']
    Sites.append(site)
Sites.reverse()

Dataset=getdatawithtablehead(Sites[0]) # 获取表头和第一个月度数据

for url in Sites[1:]:
    dataset=getdata(url)
    Dataset=numpy.row_stack((Dataset,dataset)) # 获取所有月度数据

csvfile=open("Dataset.csv","w+") # 创建csv文件用于保存数据
try:
    writer=csv.writer(csvfile)
    for i in range(numpy.shape(Dataset)[0]):
        writer.writerow((Dataset[i,:])) # 将数据逐行写入csv文件
finally:
    csvfile.close() # 关闭csv文件