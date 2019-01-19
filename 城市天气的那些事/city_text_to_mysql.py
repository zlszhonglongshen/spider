# -*- coding: utf-8 -*-
"""
Created on 2019/1/12 13:55
@Author: Johnson
@Email:593956670@qq.com
@File: city_text_to_mysql.py
"""
# 1 链接本地的数据库
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='密码', db='数据库名', charset='utf8')

# 创建表city_weather_code ，id是自增的并且唯一，同时设为主键；city_name，city_code分别对应城市名字和编码

create_table_sql = "CREATE TABLE IF NOT EXISTS city_weather_code (" \
                   "id INT PRIMARY KEY AUTO_INCREMENT," \
                   "city_name VARCHAR(30) NOT NULL ," \
                   "city_code INT NOT NULL)  "
cursor = conn.cursor()  # 获取游标
cursor.execute(create_table_sql)  # 执行创建语句
conn.commit()  # 使执行创建语句生效
# 打开文件按行读取数据
with open("city.txt", 'r', encoding='utf-8') as f:  # 读的模式打开
    res = f.readlines()  # 一行行读取文件，
    for i in res:  # 遍历文件每一行，先去空格然后以‘’=‘’号分割。每行得到一个列表
        if i != "\n":
            data = i.strip().split("=")
            citycode = data[0]  # 把编码赋值给citycode
            cityname = data[1]  # 把城市名赋值给cityname
            insert_sql = "INSERT INTO city_weather_code(city_name,city_code) VALUE ('%s','%s')" % (
            cityname.strip(), citycode.strip())  # 把数据插入数据库
            cursor.execute(insert_sql)
            conn.commit()
conn.close()
