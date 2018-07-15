#-*-coding:utf-8-*-
__author__ = 'qinlan'

import requests
from urllib.parse import urlencode
import random,os,re,time
from bs4 import BeautifulSoup
from multiprocessing import Pool


singer = '李志'

proxies = [
        '115.224.163.58:61202','179.184.9.172:20183',
        '177.37.166.164:20183','103.55.69.242:53281',
        '217.61.106.183:80','45.125.220.242:8080',
        '103.88.140.85:8080','218.26.227.108:80',
        '110.171.230.47:8080','118.81.108.77:9797',
        '31.145.83.198:8080','195.88.208.115:3128'
]

headers = {
    'host':'music.taihe.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
}

session = requests.Session()

def getMainHtml(page):#获取歌曲主页
    base_url = 'http://music.taihe.com/search/song?'
    params = {
        'key':singer,
        'start':str(page*20),
        'size':20
    }
    try:
        response = session.get(url=base_url,params=params,proxies={'https':random.choice(proxies)},headers=headers)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        else:
            print('---访问失败---')
            return None
    except:
        print('网页加载出错')
        return None

def downloadMusic(name,url):
    dir = '歌曲\{}'.format(singer)
    if not os.path.exists(dir):
        os.makedirs(dir)
    try:
        response = requests.get(url=url,proxies={'https':random.choice(proxies)})
        if response.status_code == 200:
            file = os.path.join(dir,'{}.mp3'.format(name))
            with open(file,'wb') as f:
                f.write(response.content)
            print('下载完成')
        else:
            print('状态码不为200(失败)')
    except:
        print('---%%%%---')

def getMusicLink(songid):
    base_url = 'http://play.taihe.com/data/music/songlink'
    data = {
        'songIds':songid,
        'hq':'0','type':'m4a,mp3',
        'rate':'','pt':'0',
        'flag':'-1','s2p':'-1','prerate':'-1',
        'bwt':'-1','dur':'-1','bat':'-1','bp':'-1',
        'pos':'-1','auto':'-1'
    }
    header = {
        'Host':'play.taihe.com',
        'Origin':'http://play.taihe.com',
        'referer':'http://play.taihe.com/?__m=mboxCtrl.playSong&__o=/search||songListIcon&fr=-1||www.baidu.com{}'.format(urlencode({'__a':songid,'__s':singer})),
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }
    response = session.post(url=base_url,data=data,proxies={'https':random.choice(proxies)},headers=header)
    if response.status_code == 200:
        content = response.json()
        songUrl = content['data']['songList'][0]['songLink']
        songName = content['data']['songList'][0]['songName']
        print(songName,songUrl)
        downloadMusic(songName,songUrl)
    else:
        print('---加载失败---')

def parseMusicId(html):
    if html:
        content = re.findall('sid&quot.*?(\d+),',html,re.S)
        for songid in content:
            getMusicLink(songid)
    else:
        print('------------')

def main(page):
    html = getMainHtml(page)
    parseMusicId(html)
    time.sleep(1)

if __name__ == '__main__':
    pool = Pool()
    start = time.time()
    pool.map(main,[page for page in range(1,10)])
    print('下载完毕:',time.time()-start)