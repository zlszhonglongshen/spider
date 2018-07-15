# -*- coding: utf-8 -*-

import requests
import time, os
from urllib.parse import urlencode
from multiprocessing import Pool

keyword = '车模'
headers = {
    'authority': 'www.toutiao.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    'referer': 'https://www.toutiao.com/search/?{}'.format(urlencode({'keyword': keyword})),
    'x-requested-with': 'XMLHttpRequest'
}


# 获取搜索页面
def getHtmlResponse(offset):
    base_url = 'https://www.toutiao.com/search_content/?'
    params = {
        'offset': str(offset * 20),
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3,
        'from': 'gallery'
    }
    try:
        response = requests.get(url=base_url, params=params, headers=headers)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        print('网页解析出错:', response.url)
        return None


# 解析套图
def parseGalleryPic(html):
    if html:
        content = html['data']
    for item in content:
        tag = item['tag'] if 'tag' in item.keys() else None
        title = item['title'].strip() if 'title' in item.keys() else None
        pubtime = item['datetime'] if 'datetime' in item.keys() else None
        image_list = item['image_list'] if 'image_list' in item.keys() else None
        print({'tag': tag, 'title': title, 'pubtime': pubtime})
        downloadPic(title, image_list)


# 下载单张图片
def parsePicInfo(dirname, url):
    pic_name = url.split('/')[-1]
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            pic_path = os.path.join(dirname, '{}.jpg'.format(pic_name))
            with open(pic_path, 'wb') as f:
                f.write(response.content)
    except:
        print('图片下载失败')


# 创建目录并启动套图下载
def downloadPic(title, picList):
    dirname = '{}/{}'.format(keyword, title)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    for item in picList:
        url = 'https:' + item['url']
        print('下载图片:', url)
        parsePicInfo(dirname, url)


def main(offset):
    html = getHtmlResponse(offset)
    parseGalleryPic(html)
    time.sleep(2)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [page for page in range(2)])