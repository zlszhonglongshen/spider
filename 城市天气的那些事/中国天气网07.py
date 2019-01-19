'''
@Coding: # -*- coding: utf-8 -*-
@Author: Johnson
@Date: 2019-01-12 15:22:46
@Description: 
@Email: 593956670@qq.com
'''
# -*- coding: UTF-8 -*-
import requests
import pymongo,time
import lxml
from lxml import etree
from bs4 import BeautifulSoup
month='201809'
headers={
'Cookie': 'Hm_lvt_f48cedd6a69101030e93d4ef60f48fd0=1543241829; __51cke__=; bdshare_firstime=1543241828842; ASP.NET_SessionId=qofirgu4aigcvq45zfupn045; Hm_lpvt_f48cedd6a69101030e93d4ef60f48fd0=1543241851; __tins__4560568=%7B%22sid%22%3A%201543241828606%2C%20%22vd%22%3A%204%2C%20%22expires%22%3A%201543243650598%7D; __51laig__=4',
'Host': 'www.tianqihoubao.com',
'Referer': 'http://www.tianqihoubao.com/lishi/guangzhou.html',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
}
def savedb(dbname,data):
    client = pymongo.MongoClient('127.0.0.1', 27017)  # 缺少一步骤进行属性的清洗操作，确定是否有这个值
    db = client.weather
    db[dbname].insert(data)
def gethtml(url,dbname):
    html=requests.get(url,headers=headers)#//*[@id="content"]/table/tbody/tr[3]/td[1]#//*[@id="content"]/table/tbody/tr[3]/td[1]/a
    print(html.status_code)#//*[@id="content"]/table
    soup=BeautifulSoup(html.text,"lxml")#//*[@id="content"]/table/tbody/tr[2]
    #print(soup.prettify())
    trans=soup.find_all(name='tr')##content > table > tbody > tr:nth-child(2)##content > table > tbody#//*[@id="content"]/table/tbody
    day=1
    for i in trans:
        result=i.find_all('td')
        try:
            date=result[0].a.string.replace(' ','').replace('\r\n','')
            weather=result[1].string.replace(' ','').replace('\r\n','')
            temp=result[2].string.replace(' ','').replace('\r\n','')
            wind=result[3].string.replace(' ','').replace('\r\n','')
            day=day+1
            datatem={
                'date':date,
                'weather':weather,
                'temp':temp,
                'wind':wind,
            }
            print(datatem)
            savedb(dbname,datatem)
        except TypeError:
            print('正在读取第一行')
        except AttributeError :
            print('正在读取第一行')
if __name__=='__main__':
    list=[
        "201801","201802","201803","201804","201805","201806","201807","201808","201809","201810"
    ]
    city={
        'guangzhou',
    }
    for month in list:
         url="http://www.tianqihoubao.com/lishi/wuhan/month/{month}.html".format(month=month)
         gethtml(url,'wuhan')
