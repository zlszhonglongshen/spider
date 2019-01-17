# -*- coding: utf-8 -*-
"""
Created on 2018/9/16 17:48
@author: Johnson
"""
import requests
import time
import re
from lxml import etree
import pandas as pd


#获取某市区域的所有链接
def get_areas(url):
    print("start grabing areas")
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    response = requests.get(url,headers)
    content = etree.HTML(response.text)
    areas = content.xpath("//dd[@data-index = '0']//div[@class='option-list']/a/text()")
    areas_link = content.xpath("//dd[@data-index = '0']//div[@class='option-list']/a/@href")
    for i in range(1,len(areas)):
        area = areas[i]
        area_link = areas_link[i]
        link =  'https://bj.lianjia.com' + area_link
        print("开始抓取页面")
        get_pages(area,link)

#通过获取某一区域的页数，来拼接某一页的链接
def get_pages(area,area_link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    resposne = requests.get(area_link, headers=headers)
    pages =  int(re.findall("page-data=\'{\"totalPage\":(\d+),\"curPage\"", resposne.text)[0])
    print("这个区域有" + str(pages) + "页")
    for page in range(1,pages+1):
        url = 'https://bj.lianjia.com/zufang/dongcheng/pg' + str(page)
        print("开始抓取" + str(page) +"的信息")
        get_house_info(area,url)


# 获取某一区域某一页的详细房租信息
def get_house_info(area, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}
    time.sleep(2)
    try:
        resposne = requests.get(url, headers=headers)
        content = etree.HTML(resposne.text)
        info = []
        for i in range(30):
            title = content.xpath("//div[@class='where']/a/span/text()")[i]
            room_type = content.xpath("//div[@class='where']/span[1]/span/text()")[i]
            square = re.findall("(\d+)", content.xpath("//div[@class='where']/span[2]/text()")[i])[0]
            position = content.xpath("//div[@class='where']/span[3]/text()")[i].replace(" ", "")
            try:
                detail_place = \
                re.findall("([\u4E00-\u9FA5]+)租房", content.xpath("//div[@class='other']/div/a/text()")[i])[0]
            except Exception as e:
                detail_place = ""
            floor = re.findall("([\u4E00-\u9FA5]+)\(", content.xpath("//div[@class='other']/div/text()[1]")[i])[0]
            total_floor = re.findall("(\d+)", content.xpath("//div[@class='other']/div/text()[1]")[i])[0]
            try:
                house_year = re.findall("(\d+)", content.xpath("//div[@class='other']/div/text()[2]")[i])[0]
            except Exception as e:
                house_year = ""
            price = content.xpath("//div[@class='col-3']/div/span/text()")[i]
            with open('链家北京租房.txt', 'a', encoding='utf-8') as f:
                f.write(area + ',' + title + ',' + room_type + ',' + square + ',' + position +
                        ',' + detail_place + ',' + floor + ',' + total_floor + ',' + price + ',' + house_year + '\n')

            print('writing work has done!continue the next page')

    except Exception as e:
        print('ooops! connecting error, retrying.....')
        time.sleep(20)
        return get_house_info(area, url)


def main():
    print('start!')
    url = 'https://bj.lianjia.com/zufang'
    get_areas(url)

if __name__ == '__main__':
    main()

f = open("")
df = pd.read_csv(f,sep=',',header=None,encoding='utf-8',names=['area','title','room_type','square','position','detail_place','floor','total_floor','price','house_year'])
print(df.describe())

#北京路段_房屋均价分布图

detail_place = df.groupby(['detail_place'])
house_com = detail_place['price'].agg(['mean','count'])
house_com.reset_index(inplace=True)
detail_place_main = house_com.sort_values('count',ascending=False)[0:20]

attr = detail_place_main['detail_place']
v1 = detail_place_main['count']
v2 = detail_place_main['mean']

line = Line("北京主要路段房租均价")
line.add("路段",attr,v2,is_stack=True,xaxis_rotate=30,yaxix_min=4.2,
    mark_point=['min','max'],xaxis_interval=0,line_color='lightblue',
    line_width=4,mark_point_textcolor='black',mark_point_color='lightblue',
    is_splitline_show=False)

bar = Bar("北京主要路段房屋数量")
bar.add("路段",attr,v1,is_stack=True,xaxis_rotate=30,yaxix_min=4.2,
    xaxis_interval=0,is_splitline_show=False)

overlap = Overlap()
overlap.add(bar)
overlap.add(line,yaxis_index=1,is_add_yaxis=True)
overlap.render('北京路段_房屋均价分布图.html')


#房源价格区间分布图
price_info = df[['area', 'price']]

#对价格分区
bins = [0,1000,1500,2000,2500,3000,4000,5000,6000,8000,10000]
level = ['0-1000','1000-1500', '1500-2000', '2000-3000', '3000-4000', '4000-5000', '5000-6000', '6000-8000', '8000-1000','10000以上']
price_stage = pd.cut(price_info['price'], bins = bins,labels = level).value_counts().sort_index()

attr = price_stage.index
v1 = price_stage.values

bar = Bar("价格区间&房源数量分布")
bar.add("",attr,v1,is_stack=True,xaxis_rotate=30,yaxix_min=4.2,
    xaxis_interval=0,is_splitline_show=False)

overlap = Overlap()
overlap.add(bar)
overlap.render('价格区间&房源数量分布.html')