# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 23:40:59 2018

@author: Johnson
"""

#-*-coding:utf-8-*-
__author__ = 'qinlan'

import requests
import time,os,random,re
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

base_url = 'http://www.170mv.com/mlmv'
headers = {
    'host':'www.170mv.com',
    'referer':base_url,
    'User-Agent':random.choice(agent)
}
def parseMainHtml(page):
    url = base_url + '/page/{}'.format(str(page))
    try:
        response = session.post(url=url,proxies={'https':random.choice(proxies)},headers=headers)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text
    except:
        print('GO DIE')
        return None

def parseMVlink(id):
    url = 'http://www.170mv.com/download/{}.html'.format(id)
    response = session.get(url=url,proxies={'https':random.choice(proxies)},headers=headers)
    if response.status_code == 200:
        downloadUrl = re.findall('<a.*?video_down.*?="(.*?)"',response.text,re.S)[0]
        return downloadUrl

def downloadMV(title,url):
    dir = 'MV'
    if not os.path.exists(dir):
        os.makedirs(dir)
    print(url)
    try:
        response = session.get(url=url,proxies={'https':random.choice(proxies)})
        file = os.path.join(dir,'{}.mp4'.format(title))
        with open(file,'wb') as f:
            f.write(response.content)
        print('下载完成')
    except:
        print('下载失败')


def parseMVinfo(html):
    if html:
        mvids = BeautifulSoup(html,'lxml').select('.entry-title a')
        for item in mvids:
            title = item.get_text().strip()
            id = item['href'].split('/')[-1].split('.')[0]
            print(title)
            url = parseMVlink(id)
            downloadMV(title, url)
    else:
        print('END')

def main(page):
    html = parseMainHtml(page)
    parseMVinfo(html)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[page for page in range(1,5)])