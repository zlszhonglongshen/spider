# -*- coding: utf-8 -*-
'''
@Coding: 
@Author: Johnson
@Date: 2019-01-12 14:10:19
@Description: 
@Email: 593956670@qq.com
'''
import re
from bs4 import BeautifulSoup
import requests
import pymysql
import time
 
 
# 查询代码封装成函数
def check_code(check_name):
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='as329299', db='sky',charset='utf8')
	cursor = conn.cursor()
	select_mysql = "SELECT city_code FROM city_weather_code WHERE city_name ='%s'" % check_name
	cursor.execute(select_mysql)
	res = cursor.fetchone()  # 返回值是一个元组
	# print(res)
	conn.commit()
	cursor.close()
	conn.close()
	return res[0]
 
# 拼接url封装成函数
def url(code):
	# 中国天气网址天气页面url:http://www.weather.com.cn/weather/101180101.shtml,
	# 其中101180101，即是各城市的代码。代码对应城市，拼接出地址即可
	raw_url="http://www.weather.com.cn/weather/"
	url=raw_url+str(code)+".shtml"
	return url
 
# 获取天气
def get_weather(url):
	Header ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"}
	res = requests.get(url, headers = Header)
	soup = BeautifulSoup(res.content, 'html.parser')
	# 下面代码解释出当前的日期、温度、天气、风向、风力
	# 关键是，代码写死了，爬取网站代码一改，又要跟着调整。
	data = soup.find(class_="t clearfix")
	date = data.li.h1.text
	print("查询的日期：", date)
	wea = soup.find_all(class_="wea")[0].text.strip()
	print("天气概况：", wea)
	tem = soup.find_all(class_="tem")[0].text.strip()
	print("当前温度:",tem)
	win = soup.find_all(class_="win")[0].span['title'].strip()
	print("风向:",win)
	leve1 = soup.find_all(class_="win")[0].i.text.strip()
	print("风力:",leve1)
	print("当前时间是：", time.asctime())
 
if __name__=="__main__":
	while True:
		print("--------欢迎使用py自己动手查天气--------")
		check_name = input("请输入要查询的城市[按q]退出>>>").strip()
		if check_name=="q":
			break
		else:
			try:
				code = check_code(check_name)  # 根据输入的内容数据库取对应的城市代码
				print("查询城市代码成功！")
				url = url(code)  # 拼接url
				print("正在获取天气，请稍后。。。")
				get_weather(url)  # 查询天气并输出
			except:
				print("查询失败，请输入正确的城市名称，例如[北京]、[天河]，市或区县名称。")
				
