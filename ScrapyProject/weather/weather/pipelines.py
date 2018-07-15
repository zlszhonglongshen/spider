# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import  time
import os.path
import urllib

#将获得的数据存储到txt文件
class WeatherPipeline(object):
    def process_item(self, item, spider):
        today = time.strftime('%Y%m%d', time.localtime())
        fileName = today + '.txt'
        with open(fileName,'a') as fp:
            fp.write(item['cityDate'].encode('utf8') + '\t')
            fp.write(item['week'].encode('utf8') + '\t')
            imgName = os.path.basename(item['img'])
            fp.write(imgName + '\t')
            if os.path.exists(imgName):
                pass
            else:
                with open(imgName, 'wb') as fp:
                    response = urllib.request.urlopen(item['img'])
                    fp.write(response.read())
            fp.write(item['temperature'].encode('utf8') + '\t')
            fp.write(item['weather'].encode('utf8') + '\t')
            fp.write(item['wind'].encode('utf8') + '\n\n')
            time.sleep(1)
        return item
'''
import time  
import json  
import codecs  
#将获得的数据存储到json文件  
class WeatherPipeline(object):  
    def process_item(self, item, spider):  
        today = time.strftime('%Y%m%d', time.localtime())  
        fileName = today + '.json'  
        with codecs.open(fileName, 'a', encoding='utf8') as fp:  
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'  
            fp.write(line)  
        return item  
'''


'''
import MySQLdb  
import os.path  
#将获得的数据存储到mysql数据库  
class WeatherPipeline(object):  
    def process_item(self, item, spider):  
        cityDate = item['cityDate'].encode('utf8')  
        week = item['week'].encode('utf8')   
        img = os.path.basename(item['img'])  
        temperature = item['temperature'].encode('utf8')  
        weather = item['weather'].encode('utf8')  
        wind = item['wind'].encode('utf8')  
  
        conn = MySQLdb.connect(  
                host='localhost',  
                port=3306,  
                user='crawlUSER',  
                passwd='crawl123',  
                db='scrapyDB',  
                charset = 'utf8')  
        cur = conn.cursor()  
        cur.execute("INSERT INTO weather(cityDate,week,img,temperature,weather,wind) values(%s,%s,%s,%s,%s,%s)", (cityDate,week,img,temperature,weather,wind))  
        cur.close()  
        conn.commit()  
        conn.close()  
  
        return item  

'''