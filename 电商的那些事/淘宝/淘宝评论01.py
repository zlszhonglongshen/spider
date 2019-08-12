#coding=utf-8
import re
import requests

url = 'https://s.taobao.com/search'
payload = {'q': 'python_人脸属性相关','s': '1','ie':'utf8'}  #字典传递url参数
file = open('taobao_test.txt','w',encoding='utf-8')

for k in range(0,100):        #100次，就是100个页的商品数据

    payload ['s'] = 44*k+1   #此处改变的url参数为s，s为1时第一页，s为45是第二页，89时第三页以此类推
    resp = requests.get(url, params = payload)
    print(resp.url)          #打印访问的网址
    resp.encoding = 'utf-8'  #设置编码
    title = re.findall(r'"raw_title":"([^"]+)"',resp.text,re.I)  #正则保存所有raw_title的内容，这个是书名，下面是价格，地址
    price = re.findall(r'"view_price":"([^"]+)"',resp.text,re.I)
    loc = re.findall(r'"item_loc":"([^"]+)"',resp.text,re.I)
    x = len(title)           #每一页商品的数量

    for i in range(0,x) :    #把列表的数据保存到文件中
        file.write(str(k*44+i+1)+'书名：'+title[i]+'\n'+'价格：'+price[i]+'\n'+'地址：'+loc[i]+'\n\n')


file.close()