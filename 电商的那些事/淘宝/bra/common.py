# -*- coding: utf-8 -*-
"""
Created on 2019/1/19 17:42
@Author: Johnson
@Email:593956670@qq.com
@File: common.py
"""
import requests
import time
import random
import socket
import http.client
import pymysql
import csv

#封装requests
class Common(object):
    def getUrlContent(self,url,data=None):
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'user-agent': "User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            'cache-control': 'max-age=0'} #request的请求头

        timeout = random.choice(range(80,180))
        while True:
            try:
                rep = requests.get(url,headers=header,timeout=timeout) #请求URL地址，获取返回response信息
                # rep.encoding = 'gbk'
                break
            except socket.timeout as e: #以下都是异常处理
                print('3:', e)
                time.sleep(random.choice(range(8, 15)))
            except socket.error as e:
                print('4:', e)
                time.sleep(random.choice(range(20, 60)))
            except http.client.BadStatusLine as e:
                print('5:', e)
                time.sleep(random.choice(range(30, 80)))
            except http.client.IncompleteRead as e:
                print('6:', e)
                time.sleep(random.choice(range(5, 15)))
                print('request success')
        return rep.text
    def writeData(self,data,url):
        '''返回的html全文'''
        with open(url,'a',errors='ignore',newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(data)
            print("写入成功！")

    def queryData(self,sql):
        db = pymysql.connect(host='172.20.71.35', port=3306, user='root', passwd='root', db='mysql', charset='utf8mb4')
        cursor = db.cursor()
        results = []
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
        except Exception as e:
            print("查询时发生异常"+e)
            db.rollback() #如果发生异常，则回滚
        db.close() #关闭数据库
        return results

    def insertData(self,sql):
        db = pymysql.connect(host='172.20.71.35', port=3306, user='root', passwd='root', db='mysql', charset='utf8mb4')
        cursor = db.cursor()
        try:
            # sql = "INSERT INTO WEATHER(w_id, w_date, w_detail, w_temperature) VALUES (null, '%s','%s','%s')" % (data[0], data[1], data[2])
            cursor.execute(sql)
        except Exception as e:
            print("插入时发生异常"+e)
            db.rollback()  # 如果发生异常，则回滚
        db.close()  # 关闭数据库
        print("插入数据成功!!!")
    def patchInsertData(self,sql):
        db = pymysql.connect("localhost", "zww", "960128", "test")
        cursor = db.cursor()
        try:
            # cursor.executemany('insert into WEATHER(w_id, w_date, w_detail, w_temperature_low, w_temperature_high) value(null, %s,%s,%s,%s)',datas)
            cursor.executemany(sql)
        except Exception as e:
            print("插入时发生异常"+e)
            db.rollback()  # 如果发生异常，则回滚
        db.close()  # 关闭数据库
        print("插入数据成功!!!")



