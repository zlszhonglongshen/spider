#-*-coding:utf-8-*-
__author__ = 'qinlan'

import requests
import time,os,random
from multiprocessing import Pool

keyword = '火影忍者'
proxies = [
    '115.224.163.58:61202',
    '177.37.166.164:20183',
    '103.55.69.242:53281',
    '217.61.106.183:80',
    '45.125.220.242:8080',
    '103.88.140.85:8080',
    '218.26.227.108:80',
    '110.171.230.47:8080',
    '118.81.108.77:9797',
    '60.175.212.243:33301',
    '31.145.83.198:8080',
    '179.184.9.172:20183'
]
session = requests.Session()

def getJsonHtml(pn):
    base_url = 'https://image.baidu.com/search/acjson?'
    data = {
        'tn':'resultjson_com','ipn':'rj','ct':'201326592',
        'is':'','fp':'result',
        'queryWord':keyword,
        'cl':'2','lm':'-1','ie':'utf-8','oe':'utf-8','adpicid':'',
        'st':'-1','z':'','ic':'0','word':keyword,
        's':'','se':'','tab':'','width':'','height':'','face':'0',
        'istype':'2','qc':'','nc':'1','fr':'',
        'pn':str(pn*30),'rn':'30','gsm':hex(pn*30)[2:],
        '{}'.format(str(int(time.time()*1000))):''
    }
    headers = {
        'Host':'image.baidu.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
    }
    response = session.get(url=base_url,proxies={'http':random.choice(proxies)},params=data,headers=headers)
    if response.status_code == 200:
        response.encoding = response.apparent_encoding
        return response.json()
    else:
        print('网页解析出错')
        return none

def downloadPic(id,pic_url):
    dir = '百度图片\{}'.format(keyword)
    if not os.path.exists(dir):
        os.makedirs(dir)

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
    try:
        response = session.get(url=pic_url,headers=headers)
        if response.status_code == 200:
            file = os.path.join(dir,'{}.jpg'.format(id))
            with open(file,'wb') as f:
                f.write(response.content)
    except:
        print('---图片下载失败---')

def parsePicInfo(html):
    if html:
        content = html['data']
        for item in content:
            id = item['di'] if 'di' in item.keys() else None
            pic_url = item['thumbURL'] if 'thumbURL' in item.keys() else None
            print('正在下载:',pic_url)
            if pic_url:
                downloadPic(id, pic_url)
    else:
        print('---end---')

def main(page):
    html = getJsonHtml(page)
    parsePicInfo(html)
    time.sleep(1)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[page for page in range(1,8)])