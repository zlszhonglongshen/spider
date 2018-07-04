#coding:utf-8
import requests
import time
from bs4 import BeautifulSoup
#设置列表页URL的固定部分
url='http://bj.lianjia.com/ershoufang/'
#设置页面页的可变部分
page=('pg')
#此外，还需要在很http请求中设置一个头部信息，否则很容易被封。头部信息网上有很多现成的，也可以使用httpwatch等工具来查看。具体细节按照具体情况进行调整。

#设置请求头部信息
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept':'text/html;q=0.9,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding':'gzip',
'Connection':'close',
'Referer':'http://www.baidu.com/link?url=_andhfsjjjKRgEWkj7i9cFmYYGsisrnm2A-TN3XZDQXxvGsM9k9ZZSnikW2Yds4s&amp;wd=&amp;eqid=c3435a7d00006bd600000003582bfd1f'
}
#使用for循环生成1-100的数字，转化格式后与前面的URL固定部分拼成要抓取的URL。这里我们设置每两个页面间隔0.5秒。抓取到的页面保存在html中。

#循环抓取列表页信息
for i in range(1,100):
    if i==1:
        i=str(i)
        a=(url+page+i+'/')
        r=requests.get(url=a,headers=headers)
        html=r.content
    else:
        i=str(i)
        a=(url+page+i+'/')
        r=requests.get(url=a,headers=headers)
        html2=r.content
        html=html+html2
    #每隔0.5秒
    time.sleep(0.5)
#页面抓取完成后无法直接阅读和进行数据提取，还需要进行页面解析。我们使用BeautifulSoup对页面进行解析。变成我们在浏览器查看源代码中看到的样子。

#解析抓取的页面内容
lj=BeautifulSoup(html,'html.parser')

#把页面div标签中class=priceInfo的部分提取出来，并使用for循环将其中每个房源的总价数据存在tp中。pric
price=lj.find_all('div',attrs={'class':'priceInfo'})
tp=[]
for a in price:
    totalPrice=a.span.string
    tp.append(totalPrice)

#提取房源信息
houseInfo=lj.find_all('div',attrs={'class':'houseInfo'})

hi=[]
for b in houseInfo:
    house=b.get_text()
    hi.append(house)
#提取房源关注度
followInfo=lj.find_all('div',attrs={'class':'followInfo'})

fi=[]
for c in followInfo:
    follow=c.get_text()
    fi.append(follow)

import pandas as pd

house=pd.DataFrame({'totalprice':tp,'houseinfo':hi,'followinfo':fi})
print (house.head())
houseinfo_split = pd.DataFrame((x.split('|') for x in house.houseinfo),index=house.index,columns=['xiaoqu','huxing','mianji','chaoxiang','zhuangxiu','dianti'])
print (houseinfo_split.head())
#将分列结果接回原始数据表
house=pd.merge(house,houseinfo_split,right_index=True,left_index=True)
#对房源关注度进行分列
followinfo_split = pd.DataFrame((x.split('/') for x in house.followinfo),index=house.index,columns=['guanzhu','daikan','fabu'])
#将分列后的关注度信息拼接回原数据表
house=pd.merge(house,followinfo_split,right_index=True, left_index=True)
print(house)
