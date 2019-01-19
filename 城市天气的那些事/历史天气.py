#coding:utf-8

import urllib2
import random
import io
import csv
import datetime
from bs4 import BeautifulSoup

my_headers = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)        Chrome/48.0.2564.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)   Chrome/45.0.2454.101 Safari/537.36"
        ]

def get_content(url, headers):
    '''
    随机选择my_headers中一个模拟浏览器访问
    '''
    random_header = random.choice(headers)
    request = urllib2.Request(url)
    request.add_header("User-Agent", random_header)
    request.add_header("Host", "lishi.tianqi.com")
    request.add_header("Referer", "http://lishi.tianqi.com/")
    request.add_header("GET", url)

    html = urllib2.urlopen(request)
    content = html.read().decode("gbk").encode("utf-8")
    html.close()
    return content

def get_link(html_text):
    '''
    获取所有的链接
    http://lishi.tianqi.com/beijing/201603.html
    http://lishi.tianqi.com/beijing/201602.html
    '''
    link_list = []
    bs = BeautifulSoup(html_text, "html.parser")
    div = bs.find_all('div', {'id': 'tool_site'})
    link = div[4].find_all('a')
    for x in link:
        link_list.append(x.get("href"))
        print x.get("href"), x.string
    return link_list

def get_data(html_text):
    '''
    得到每天的数据
    bs.find('div', {'class': 'tqtongji2'})
    '''
    result = []
    bs = BeautifulSoup(html_text, "html.parser")

    content = bs.find('div', {'class': 'tqtongji2'})
    ul = content.find_all("ul")
    for x in ul:
        if x != ul[0]:
            temp = []
            data = x.find_all("li")
            date = data[0].string
            high = data[1].string
            low = data[2].string
            weather = data[3].string
            wind_direction = data[4].string
            '''
            输出到.txt文件中时发现出现格式错误，
            原因是wind_direction为空，
            '''
            if wind_direction is None:
                wind_direction = "Null"
            wind_force = data[5].string

            temp.append(date)
            temp.append(high)
            temp.append(low)
            temp.append(weather)
            temp.append(wind_direction)
            temp.append(wind_force)
            result.append(temp)
    return result
#
# def write_data(data, name):
#     '''
#     写入到csv文件中
#     如果想输出到指定位置
#     url = 'C:\\Users\\Administrator\\Desktop\\'
#     with open(url + name, "ab") as f:
#         写入到桌面
#     '''
#     with io.open(name, "ab",encoding="utf-8") as f:
#         f_csv = csv.writer(f)
#         f_csv.writerows(data)


def write_data(data, name):
    '''
    写入到txt文件中
    '''
    for x in data:
        for i in x:
            if i is None:
                i = "Null"
            fw = io.open(name, "ab",encoding="utf-8")
            fw.write(i + "\t")
        fw.write("\n")
    fw.close()


url = "http://lishi.tianqi.com/beijing/index.html"

'''
程序运行的开始时间
'''
start_time = datetime.datetime.now()
print start_time

'''
得到html内容
'''
content = get_content(url, my_headers)

'''
得到每年月份的链接
'''
link = get_link(content)

'''
循环每年月日的链接得到数据，并写入到文件中
'''
for x in link:
    html_text = get_content(x, my_headers)
    data = get_data(html_text)
    file_name = "weather.csv"   #保存的文件名
    write_data(data, file_name)

'''
程序的结束时间
'''
endtime = datetime.datetime.now()
print endtime

'''
程序的总运行时间(秒)
'''
print (endtime - start_time).seconds