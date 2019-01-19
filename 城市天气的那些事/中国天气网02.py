# -*- coding: utf-8 -*-
"""
Created on 2019/1/12 0:02
@author: Johnson
Email:593956670@qq.com
@software: PyCharm
"""
import requests
from lxml import etree

headers = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'


def get_html(url):
    try:
        html = requests.get(url, headers={'User-Agent': 'headers'})
        html.encoding = html.apparent_encoding
        if html.status_code == 200:
            return html.text
        return 0

    except RequestsException:
        return 0


'''
conMintab:  华北  
    conMintab2    北京
    conMintab2    天津
    conMintab2    河北
    conMintab2    山西
    conMintab2    内蒙古


//div[@class="conMidtab"][1] 今天
//div[@class="conMidtab"][2] 明天 
                ...
//div[@class="conMidtab"][7] 最后一天
'''


def parse_html(html):
    wea = []
    html_element = etree.HTML(html)
    # !!!!!  trs = html_element.xpath('//div[@class="conMidtab"][1]//tr')[2:]
    provinces = html_element.xpath('//div[@class="conMidtab"][1]//div[@class="conMidtab2"]')
    for province in provinces:
        trs = province.xpath('.//tr')[2:]
        for tr in trs:
            weather = {}
            city = tr.xpath('.//td[@width="83"]/a/text()')
            phenomenon = tr.xpath('.//td[@width="89"]/text()')
            wind = tr.xpath('.//td[@width="162"]//text()')
            hightest = tr.xpath('.//td[@width="92"]/text()')
            weather['city'] = city
            weather['phenomenon'] = phenomenon
            weather['wind'] = wind
            weather['hightest'] = hightest
            while '\n' in wind:
                wind.remove('\n')
            wea.append(weather)

    print(wea)


def main():
    urls = ['http://www.weather.com.cn/textFC/hb.shtml',
            'http://www.weather.com.cn/textFC/db.shtml',
            'http://www.weather.com.cn/textFC/hd.shtml',
            'http://www.weather.com.cn/textFC/hz.shtml',
            'http://www.weather.com.cn/textFC/hn.shtml',
            'http://www.weather.com.cn/textFC/xb.shtml',
            'http://www.weather.com.cn/textFC/xn.shtml',
            'http://www.weather.com.cn/textFC/gat.shtml']
    for url in urls:
        html = get_html(url)
        if html == 0:
            html = get_html(url)
        parse_html(html)


if __name__ == '__main__':
    main()