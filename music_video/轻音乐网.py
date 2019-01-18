# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 23:43:19 2018

@author: Johnson
"""


import requests
import time,os,random,pymongo
from prettytable import PrettyTable as pt
from bs4 import BeautifulSoup
from multiprocessing import Pool

proxies = [
        '115.224.163.58:61202','179.184.9.172:20183',
        '177.37.166.164:20183','103.55.69.242:53281',
        '217.61.106.183:80','45.125.220.242:8080',
        '103.88.140.85:8080','218.26.227.108:80',
        '110.171.230.47:8080','118.81.108.77:9797',
        '31.145.83.198:8080','195.88.208.115:3128'
]

agent = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24'
]

session = requests.Session()

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
}

'''
纯音乐:http://www.htqyy.com/genre/1
新世纪:http://www.htqyy.com/genre/2
钢琴曲:http://www.htqyy.com/genre/3
减压放松:http://www.htqyy.com/genre/4
中国音乐:http://www.htqyy.com/genre/5
天籁之音:http://www.htqyy.com/genre/6
影视原声:http://www.htqyy.com/genre/7
电子乐:http://www.htqyy.com/genre/8
'''

def parseMainHtml(pn):
    base_url = 'http://www.htqyy.com/genre/musicList/1?'
    params = {
        'pageIndex':str(pn),
        'pageSize': '20',
        'order': 'hot'

    }
    try:
        response = session.get(url=base_url,params=params,proxies={'https':random.choice(proxies)},headers=headers)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text
    except:
        print('---GO DIE---')
        return None

def downloadMusic(songName,songId):
    dir = '歌曲'
    if not os.path.exists(dir):
        os.makedirs(dir)
    url = 'http://f2.htqyy.com/play7/{}/mp3/7'.format(songId)
    try:
        response = session.get(url=url,proxies={'https':random.choice(proxies)},headers=headers)
        if response.status_code == 200:
            file = os.path.join(dir, '{}.mp3'.format(songName))
            with open(file, 'wb') as f:
                f.write(response.content)
        else:
            url = 'http://f2.htqyy.com/play7/{}/m4a/7'.format(songId)
            response = session.get(url=url, proxies={'https': random.choice(proxies)}, headers=headers)
            file = os.path.join(dir, '{}.mp3'.format(songName))
            with open(file, 'wb') as f:
                f.write(response.content)
    except:
        print('下载失败')

def parseSongInfo(html):
    if html:
        soup = BeautifulSoup(html,'lxml').select('.mItem .title a')
        for item in soup:
            songName = item.get_text().strip()
            songId = item['sid']
            print('下载歌曲:',songName)
            downloadMusic(songName,songId)
    else:
        print('END')

def main(offset):
    html = parseMainHtml(offset)
    parseSongInfo(html)

if __name__ == '__main__':
    pool = Pool()
    start = time.time()
    pool.map(main,[offset for offset in range(0,10)])
    print('下载完毕:',time.time()-start)