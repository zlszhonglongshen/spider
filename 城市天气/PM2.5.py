# coding=utf-8
import os
import types
import urllib2
import json
import csv
import time

# csv file path
LOCAL_DATA_PATH = "./json_data/"

# all file path
LOCAL_HTML_ALL_PATH = './all/'

# rank file path
LOCAL_HTML_RANK_PATH = './rank/'

# windows path
WINDOWS_PATH = './windows/'


class Weather(object):


	def __init__(self):
		token = "wxwpmNWzXxc2syn697pM"
		self.url_all = "http://www.pm25.in/api/querys/all_cities.json?token=%s" % token
		self.url_rank = "http://www.pm25.in/api/querys/aqi_ranking.json?token=%s" % token


	#利用urllib2获取网络数据
	def get_data(self):
		try:
			data_all = urllib2.urlopen(self.url_all).read()
			data_rank = urllib2.urlopen(self.url_rank).read()
			self.save_origin_file(data_all, data_rank)
			value = json.loads(data_rank)
			return value
		except Exception, e:
			print e

	def save_origin_file(self, data_all, data_rank):
		localtime   = time.localtime()
		timestring = time.strftime("%Y-%m-%d-%H", localtime)
		html_all = open((LOCAL_HTML_ALL_PATH+timestring), 'w')
		html_rank = open((LOCAL_HTML_RANK_PATH+timestring), 'w')
		html_all.write(data_all)
		html_rank.write(data_rank)


	def write_csv_data(self, value):
		for detail in value:
			data = self.praserjsonfile(detail)
			writer = csv.writer(open((LOCAL_DATA_PATH+detail['area'])+'.csv', 'ab'))
			writer.writerow(data)

	def praserjsonfile(self, detail):
		return [detail['time_point'], detail['aqi'], detail['co'], detail['co_24h'], \
					detail['no2'], detail['no2_24h'], detail['o3'], detail['o3_24h'], detail['o3_8h'], \
					detail['o3_8h_24h'], detail['pm10'], detail['pm10_24h'], detail['pm2_5'], detail['pm2_5_24h'], \
					detail['so2'], detail['so2_24h']]


	def write_csv_head(self, area):
		writer=csv.writer(open((LOCAL_DATA_PATH+area)+'.csv', 'ab'))
		writer.writerow(['time_point', 'aqi','co', 'co_24h', 'no2', 'no2_24h',\
			'o3', 'o3_24h', 'o3_8h', 'o3_8h_24h', 'pm10', 'pm10_24h',\
			'pm2_5', 'pm2_5_24h', 'so2', 'so2_24h'])


def convert_to_windows():
	import shutil
	from city_json import *

	for file in os.listdir(LOCAL_DATA_PATH):
		new_file = "%s%s" %(city[file.split('.')[0]],'.csv')
		shutil.copy2(LOCAL_DATA_PATH+file, WINDOWS_PATH+new_file)


if __name__ == "__main__":

	if not os.path.exists(LOCAL_DATA_PATH):
		os.mkdir(LOCAL_DATA_PATH)

	if not os.path.exists(LOCAL_HTML_ALL_PATH):
		os.mkdir(LOCAL_HTML_ALL_PATH)

	if not os.path.exists(LOCAL_HTML_RANK_PATH):
		os.mkdir(LOCAL_HTML_RANK_PATH)

	if not os.path.exists(WINDOWS_PATH):
		os.mkdir(WINDOWS_PATH)


	weather = Weather()
	data = weather.get_data()
	print data

	######## 第一次运行的时候写入csv的头, 以后都不需要运行 #######
	# for detail in data:
		# weather.write_csv_head(detail['area'])
	#########################################

	weather.write_csv_data(data)
	# windows 编码 可能会有问题，所以将城市名转成拼音
	convert_to_windows()