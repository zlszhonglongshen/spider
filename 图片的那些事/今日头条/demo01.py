# -*- coding: utf-8 -*-
import os
import re
import json
import requests
from urllib.parse import urlencode


def get_one_page(offset, keyword):
    '''
    获取网页html内容并返回
    '''
    paras = {
        'offset': offset,  # 搜索结果项开始的位置
        'format': 'json',  # 返回的数据格式
        'keyword': keyword,  # 搜索的关键字
        'autoload': 'true',  # 自动加载
        'count': 20,  # 每次加载结果的项目数
        'cur_tab': 3,  # 当前的tab页索引，3为“图集”
        'from': 'gallery'  # 来源，“图集”
    }

    url = 'https://www.toutiao.com/search_content/?' + urlencode(paras)
    try:
        # 获取网页内容，返回json格式数据
        response = requests.get(url)
        # 通过状态码判断是否获取成功
        if response.status_code == 200:
            return response.text
        return None
    except Exception:
        return None


def parse_one_page(html):
    '''
    解析出组图网址,并将网页中所有图集的标题及图片地址返回
    '''
    urls = []
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            page_urls = []
            title = item.get('title')
            image_detail = item.get('image_list')
            for i in range(len(image_detail)):
                # 获取large图片地址
                url = image_detail[i]['url']
                # 替换URL获取高清原图
                url = url.replace('list', 'origin')
                url = "http:"+url
                page_urls.append(url)
            urls.append({'title': title, 'url_list': page_urls})
    return urls


def save_image_file(url, path):
    '''
    保存图像文件
    '''
    ir = requests.get(url)
    if ir.status_code == 200:
        with open(path, 'wb') as f:
            f.write(ir.content)
            f.close()


def main(offset, word):
    html = get_one_page(offset, word)
    urls = parse_one_page(html)

    # 图像文件夹不存在则创建
    root_path = word
    if not os.path.exists(root_path):
        os.mkdir(root_path)

    for i in range(len(urls)):
        print('---正在下载 %s' % urls[i]['title'])
        folder = root_path + '/' + urls[i]['title']
        if not os.path.exists(folder):
            try:
                os.mkdir(folder)
            except NotADirectoryError:
                continue
            except OSError:
                continue

        url_list = urls[i]['url_list']
        for j in range(len(url_list)):
            path = folder + '/index_' + str("%02d" % j) + '.jpg'
            if not os.path.exists(path):
                save_image_file(urls[i]['url_list'][j], path)


if __name__ == '__main__':
    # 抓取2000个图集，基本上包含全部图集
    for i in range(100):
        main(i * 20, '街拍')
