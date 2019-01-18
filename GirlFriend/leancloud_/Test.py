# -*- coding: utf-8 -*-
"""
Created on 2019/1/18 15:45
@Author: Johnson
@Email:593956670@qq.com
@File: Test.py
"""
import leancloud
import datetime
import requests
from lxml.html import etree
import json

city_name = "广州"

index_url = "http://tianqi.moji.com/api/citysearch/%s" % city_name  # 构造查询相应城市天气的url
response = requests.get(index_url)
response.encoding = "utf-8"
try:  # 异常捕获
    city_id = json.loads(response.text).get('city_list')[0].get('cityId')  # 通过上面的url获取城市的id
    city_url = "http://tianqi.moji.com/api/redirect/%s" % str(city_id)  # 通过城市id获取城市天气
except:
    print('城市名输入错误')
    exit()

response = requests.get(city_url)
if not response.status_code == 200:
    print('天气详情请求错误：' + str(response.status_code))


# 对获取到的req格式化操作，方便后面用xpath解析
sel = etree.HTML(response.text)
# 查询城市
location = sel.xpath('//div[@class="search_default"]/em/text()')[0]
# 今日天气提醒
tip = sel.xpath('//div[@class="wea_tips clearfix"]/em/text()')[0]
# 天气情况
# weathers = sel.xpath('//div[@class="forecast clearfix"]/ul[@class="days clearfix"]/li/text()')[0].extract()

# 空气质量
air = '空气质量' + sel.xpath('//div[@class="wea_alert clearfix"]/ul/li/a/em/text()')[0]

# 天气类型
weather_type = sel.xpath('//div[@class="wea_weather clearfix"]/em/text()')[0] + '°C'
# 温度范围
temperature_range = sel.xpath('//div[@class="wea_weather clearfix"]/b/text()')[0]
# 湿度
humidity = sel.xpath('//div[@class="wea_about clearfix"]/span/text()')[0]
# 风向
wind_direction = sel.xpath('//div[@class="wea_about clearfix"]/em/text()')[0]



#计算相恋天数
inLoveDate = datetime.datetime(2018, 10,27)
todayDate = datetime.datetime.today()
inLoveDays = (todayDate - inLoveDate).days
print('我们相恋了' + str(inLoveDays) + '天')


leancloud.init("y796vyvMbGIVkXM0EbLQnNlT-gzGzoHsz", "823GykQe9jmI2TmNppuz7pbY")

# 初始化leancloud对象
LoveWords = leancloud.Object.extend('LoveWords')
LovePhoto = leancloud.Object.extend('LovePhoto')
# 计算发送天数
beginSendDate = datetime.datetime(2017, 12, 15)
todaySendDate = datetime.datetime.today()
sendDays = (todaySendDate - beginSendDate).days + 1
# 查询情话
query = LoveWords.query
query.equal_to('id', sendDays)
loveWord = query.first().get('loveWord')
# 查询图片
query = LovePhoto.query
query.equal_to('id', sendDays)
lovePhotoSrc = query.first().get('lovePhotoSrc')

weather_detail = weather_type + temperature_range + '|' + air + '|' + humidity + '|' + wind_direction

print(weather_detail,loveWord)

print("测试成功")