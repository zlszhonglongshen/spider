#-*-coding:utf-8-*-
__author__ = 'qinlan'

import requests
import time,os,random,re,json
from multiprocessing import Pool

keyword = 'Linkin Park'

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


headers = {
        'referer':'https://y.qq.com/portal/search.html',
        'User-Agent':random.choice(agent)
    }

session = requests.Session()

def parseMainHtml(page):
    base_url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?'
    params = {
        #URL可变参数如下:p(页码)+w(关键词)+jsonpCallback(Math.random()*16)
        'p':str(page),'n':'20','w':keyword,
        'jsonpCallback':'MusicJsonCallback2378952422470939'
    }
    try:
        response = session.get(url=base_url,params=params,proxies={'http':random.choice(proxies)},headers=headers)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        else:
            print('状态码不为200(失败)')
            return None
    except:
        print('网页加载出错')
        return None

#下载单首歌曲
def downloadMusic(name,music_url):
    dir = keyword
    if not os.path.exists(dir):
        os.makedirs(dir)
    print('正在下载:',music_url)
    response = session.get(url=music_url,proxies={'https':random.choice(proxies)},headers=headers)
    if response.status_code == 200:
        #判断MP3文件名合法
        if '|' or '/' or '"' in name:
            name = name.replace('|','')
            name = name.replace('/', '')
            name = name.replace('"', '')
        file = os.path.join(dir,'{}.mp3'.format(name))
        with open(file,'wb') as f:
            f.write(response.content)
    else:
        print('---歌曲下载失败---')

#获取关键参数songmid
def parseMusicLink(name,songmid):
    base_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?'
    params = {
        'g_tk':'2050600154',
        'jsonpCallback':'MusicJsonCallback6404852530578047',
        'loginUin':'0',
        'hostUin':'0',
        'format':'json',
        'inCharset':'utf8',
        'outCharset':'utf-8',
        'notice':'0',
        'platform':'yqq',
        'needNewCode':'0',
        'cid':'205361747',
        'callback':'MusicJsonCallback6404852530578047',
        'uin':'0',
        'songmid': songmid,
        'filename':'C400'+songmid+'.m4a',
        'guid':'704849852'
    }
    response = session.get(url=base_url,params=params,proxies={'http':random.choice(proxies)},headers=headers)
    if response.status_code == 200:
        content = re.findall('\(({.*})\)',response.text)[0]
        content = json.loads(content)
        vkey = content['data']['items'][0]['vkey'] if content['data']['items'] else None
        if vkey:
            music_url = 'http://202.201.0.82:9999/dl.stream.qqmusic.qq.com/' + 'C400' + songmid + '.m4a' \
                        + '?vkey={}'.format(vkey) + '&uin=0&guid=704849852&fromtag=66'
            downloadMusic(name, music_url)
    else:
        print('状态码不为200(失败)')

def parseMusicInfo(html):
    if html:
        content = re.findall('\(({.*})\)',html,re.S)[0]
        content = json.loads(content)['data']['song']['list']
        for item in content:
            name = item['songname']
            songmid = item['songmid']
            parseMusicLink(name, songmid)
    else:
        print('---end---')

def main(page):
    html = parseMainHtml(page)
    parseMusicInfo(html)
    time.sleep(1)

if __name__ == '__main__':
    pool = Pool()
    start = time.time()
    pool.map(main,[page for page in range(1,5)])
    print('下载完毕:',time.time()-start)