#coding:utf-8
import urllib2
import urllib
import requests
import re
import time



# 设置请求头
headers = {'Accept':'*/*','Accept-Encoding':'gzip, deflate','Accept-Language':'zh-CN,zh;q=0.9','Connection':'keep-alive','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
          }
# 拼接URL，用于翻页爬虫
url_phase1 = 'http://www.cmbchina.com/cfweb/svrajax/product.ashx?op=search&type=m&pageindex='
url_phase2 = '&salestatus=&baoben=&currency=&term=&keyword=&series=01&risk=&city=&date=&pagesize=40&orderby=ord1&t=0.8683289736280901'

urls = []
for i in range(1,29):
    urls.append(url_phase1+str(i)+url_phase2)

#构造空列表，用于后面数据存储
Finacing = []

#利用for循环完成url的遍历
for url in urls:
    #获取源码
    text = requests.get(url,headers=headers).text
    # 正则表达式完成信息的获取
    ProdCode = re.findall('PrdCode:"(.*?)",', text)
    ProdName = re.findall('PrdName:"(.*?)",', text)
    TypeCode = re.findall('TypeCode:"(.*?)",', text)
    AreaCode = re.findall('AreaCode:"(.*?)",', text)
    BeginDate = re.findall('BeginDate:"(.*?)",', text)
    EndDate = re.findall('EndDate:"(.*?)",', text)
    ExpireDate = re.findall('ExpireDate:"(.*?)",', text)
    Status = re.findall('Status:"(.*?)",', text)
    NetValue = re.findall('NetValue:"(.*?)",', text)
    IsNewFlag = re.findall('IsNewFlag:"(.*?)",', text)
    NetValue = re.findall('NetValue:"(.*?)",', text)
    Term = re.findall('Term:"(.*?)",', text)
    Style = re.findall('Style:"(.*?)",', text)
    InitMoney = re.findall('InitMoney:"(.*?)",', text)
    IncresingMoney = re.findall('IncresingMoney:"(.*?)",', text)
    Risk = re.findall('Risk:"(.*?)",', text)
    FinDate = re.findall('FinDate:"(.*?)",', text)
    SaleChannel = re.findall('SaleChannel:"(.*?)",', text)
    SaleChannelName = re.findall('SaleChannelName:"(.*?)",', text)
    IsCanBuy = re.findall('IsCanBuy:"(.*?)"}', text)

    # 数据存储到字典中
    Finacing.append({'ProdCode': ProdCode, 'ProdName': ProdName, 'TypeCode': TypeCode, 'AreaCode': AreaCode,
                     'BeginDate': BeginDate, 'EndDate': EndDate, 'ExpireDate': ExpireDate, 'Status': Status,
                     'NetValue': NetValue, 'IsNewFlag': IsNewFlag, 'NetValue': NetValue, 'Term': Term,
                     'Style': Style, 'InitMoney': InitMoney, 'IncresingMoney': IncresingMoney, 'Risk': Risk,
                     'FinDate': FinDate, 'SaleChannel': SaleChannel, 'SaleChannelName': SaleChannelName,
                     'IsCanBuy': IsCanBuy})

    # 睡眠3秒
    time.sleep(3)
import pandas as pd

#将数据转化为数据框
MB_Fiance= pd.concat([pd.DataFrame(data)] for data in Finacing)
print(MB_Fiance.head())
for data in Finacing:
    pd.concat([pd.DataFrame(data)])