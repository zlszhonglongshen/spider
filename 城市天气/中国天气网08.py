# -*- coding: utf-8 -*-
"""
Created on 2019/1/12 17:59
@Author: Johnson
@Email:593956670@qq.com
@File: 中国天气网08.py
"""
import requests, csv, random, time, socket
from bs4 import BeautifulSoup
import http.client

def get_content(url, data = None):
    header = {
    'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8',
    'Accept - Encoding':'gzip, deflate, sdch',
    'Accept - Language':'zh - CN, zh;q = 0.8',
    'Connection':'keep - alive',
    'User - Agent': 'Mozilla / 5.0(Macintosh;Intel Mac OS X 10 11_6) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 50.0.2661.102Safari / 537.36'
    }
    timeout = random.choice(range(80,180))
    while True:
        try:
            rep = requests.get(url, headers = header, timeout = timeout)
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print('3:', e)
            time.sleep(random.choice(range(8,15)))

        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20,60)))

        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30,80)))

        except http.client.ImproperConnectionState as e:
            print('6:', e)
            time.sleep(random.choice(range(5,15)))

    return rep.text

def get_data(html_text):
    finalFile = []
    bs = BeautifulSoup(html_text, 'html.parser')
    body = bs.body
    data = body.find('div', id="15d")
    ul = data.find('ul')
    li = ul.find_all('li')

    for day in li:
        temp = []
        inf = day.find_all('span')

        date = inf[0].string
        temp.append(date)

        weather = inf[1].string
        temp.append(weather)

        temperature= inf[2].text
        temp.append(temperature)

        wind = inf[3].string
        temp.append(wind)

        wind1 = inf[4].string
        temp.append(wind1)

        finalFile.append(temp)

    return finalFile

def write_data(data, name):
    file_name = name
    with open(file_name, 'a', errors = 'ignore', newline = '') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)

if __name__ == '__main__':
    url = 'http://www.weather.com.cn/weather15d/101270101.shtml'
    html = get_content(url)
    print(html)
    result = get_data(html)
    write_data(result, 'e:/content.csv')