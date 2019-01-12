# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 15:51:46 2019

@author: johnson.zhong
"""
import threading
import urllib
import re,sys
import time
import hashlib
import os
from urllib.request import urlopen
 
 
def fetchdata(city):
    print (city)
    md5 = ''
    while True:
        temp='http://www.pm25.in/'+ city#爬虫的站为：www.pm25.in,只要之前IP没有被该网站封了，就可以爬，假如被封了请申请API
        url = urlopen(temp)
        text = url.read().decode("utf-8")
#        print(text.decode("utf-8"))
        
        shuju = re.findall('<td>(.*?)</td>',text,re.S)#正则pm2.5等污染物数据
        data_time = re.findall("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",text,re.S)#正则寻找当前时间 例如，2016-04-13 20:10:00
 
 
#        md52 = hashlib.md5()
#        md52.update(data_time[0])
# 
#        if md52.hexdigest() == md5:
#            time.sleep(3600)#自动休眠，每一小时爬一次数据
#            continue
#        md5 = md52.hexdigest()
        
        i = 1
        j = 0
        datas = []
        tempdata = open('D:/'+ city + '.txt','a')#在该路径下创建以城市命名的文件，以存储pm2.5数据
        for each in shuju:
            datas.append(each)
            i += 1
            if i > 10:
                datas.append(data_time[0])
                i = 1
                j += 1
                tempdata.write(','.join(datas) + '\n')
                datas = []
         
        tempdata.close()
        print (city)
        print (data_time[0])
        print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))#显示当前时间
        time.sleep(3600)

def mkdir(path):
        print(path)
        folder = os.path.exists(path)
        if not folder:
                os.makedirs(path)
        else:
                "文件夹已经存在！"
                
 
if __name__ == "__main__":
#    file = open('D:/cities.txt','r')#读取城市名字txt，每行为一个名字
#    lines= file.readlines()
#    cities = []
#    threads = []
#    for line in lines:
#        cities.append(line.strip())
    threads = []
    cities = ["shenzhen"]
         
    for city in cities:
        threads.append(threading.Thread(target = fetchdata,args =(city,)))
 
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
