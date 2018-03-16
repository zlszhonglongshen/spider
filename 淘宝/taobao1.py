#coding:utf-8
import re
import time
import requests
import pandas as pd
from retrying import retry
from concurrent.futures import ThreadPoolExecutor

start = time.time() #start time

plist = []

for i in range(1,101):
    j =  44*(i-1)
    plist.append(j)


listno = plist
datatmsp = pd.DataFrame(columns=[])

while True:
    @retry(stop_max_attempt_number = 8)
    def network_programming(num):
        url = ''+str(num)
        web = requests.get(url,headers=headers)
        web.encoding = 'utf-8'
        return web
    headers = {} #修改headers参数

    def multithreading():
        number = listno
        event = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for result in executor.map(network_programming,number,chunksize=10):
                event.append(result)
        return event

    listpg = []
    event = multithreading()
    for i in event:
        json = re.findall('"auctions":(.*?),"recommendAuctons"',i.text)
        if len(json):
            table = pd.read_json(json[0])
            datatmsp = pd.concat([datatmsp,table],axis=0,ignore_index=True)
            pg = re.findall('"pageNum":(.*?),"p4pbottom_up"',i.text)[0]
            listpg.append(pg)

    lists = []
    for a in listpg:
        b = 44*(int(a)-1)
        lists.append(b) #将爬取成功的页码转化为URL中的num值

    listn = listno

    listno = []

    for p in listn:
        if p not in lists:
            listno.append(p)

    if len(listno)==0: #当未爬取页数为0时，终止循环！
        break


datatmsp.to_excel('datatmsp.xls',index=False)

end = time.clock()
print("爬取完成用时：",end-start,'s')

