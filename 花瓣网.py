#-*-coding:utf-8-*-
__author__ = 'qinlan'

import requests
from urllib.parse import urlencode
import random,re,json,os,time
from multiprocessing import Pool

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'Referer':'http://huaban.com/',
    'Origin':'http://huaban.com',
    'X-Request':'JSON',
    'X-Requested-With':'XMLHttpRequest'
}
proxies = [
    '115.224.163.58:61202',
    '177.37.166.164:20183',
    '217.61.106.183:80',
    '103.88.140.85:8080',
    '95.0.219.105:8080',
    '188.211.227.253:53281'
]

keyword = '建筑'

if not os.path.exists(keyword):
    os.makedirs(keyword)

session = requests.Session()

def login():
    data = {
        'email': '15292611130',
        'password': 'ql18883283303',
        '_ref': 'frame'
    }
    login_url = 'https://huaban.com/auth/'
    response = requests.post(url=login_url,data=data,proxies={'http':random.choice(proxies)},headers=headers)
    response.encoding = response.apparent_encoding
    if response.status_code == 200:
        print('---登陆成功---')
    else:
        print('---登录失败---')

def getParseHtml(page):
    url = 'http://huaban.com/search/?'
    headers = {
        'Host':'huaban.com',
        'Referer':'http://huaban.com/search/?{}'.format(urlencode({'q':keyword})),
        'X-Request':'JSON',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
    params = {
        'q':keyword,
        'jitvaawj':'',
        'page':str(page),
        'per_page':'20',
        'wfl':'1'
    }
    response = session.get(url=url,params=params,headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print('网页加载出错')

def downloadPic(pic_url,key):
    headers = {
        'Host':'img.hb.aicdn.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
    response = session.get(url=pic_url,proxies={'https':random.choice(proxies)},headers=headers)
    if response.status_code == 200:
        filename = os.path.join(keyword,'{}.jpg'.format(key))
        with open(filename,'wb') as f:
            f.write(response.content)

def parsePicUrl(html):
    if html:
        content = re.findall('app.page\["pins"\].*?\[({.*})\].*?app.page\["page"\]',html,re.S)[0]
        keys = re.findall('"key":"(.*?)",',content,re.S)
        for key in keys:
            url = 'http://img.hb.aicdn.com/{}_fw658'.format(key)
            print('正在下载:',url)
            downloadPic(url,key)
            time.sleep(1)

login()

def main(page):
    html = getParseHtml(page)
    parsePicUrl(html)

if __name__=='__main__':
    pool = Pool()
    pool.map(main,[page for page in range(1,5)])