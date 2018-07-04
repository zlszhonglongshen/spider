#coding:utf-8
import requests
from bs4 import BeautifulSoup
def get_one_page(url):
    wb_data = requests.get(url)
    wb_data.encoding = wb_data.apparent_encoding
    if wb_data.status_code == 200:
        return wb_data.text
    else:
        return None


def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')

    titles = soup.select('div.mode-box.classfiy-box div.video-pic-list ul li a div.txt h6')
    nums = soup.select('div.mode-box.classfiy-box div.video-pic-list ul li a div.video-set span.look-icon')
    hosts = soup.select(
        'div.mode-box.classfiy-box div.video-pic-list ul li a div.video-set span.person-icon.subStrTitle')
    tvs = soup.select('div.mode-box.classfiy-box div.video-pic-list ul li a div.video-set span.tv')

    wb_data = []
    for title, num, host, tv in zip(titles, nums, hosts, tvs):
        data = {
            '标题': title.get_text(),
            '观看人数': num.get_text(),
            '主播': host.get_text(),
            '平台': tv.get_text()
        }
        wb_data.append(data)
    return wb_data

textArea = []
def add_text(url):
    # url = 'http://www.laoyuegou.com/media_v2/live/index/page/1.html'
    html = get_one_page(url)
    wb_data = parse_one_page(html)
    for item in wb_data:
        textArea.append(str(item))
    return textArea

def get_text():
    for i in range(1, 10):
        url = 'http://www.laoyuegou.com/media_v2/live/index/page/' + str(i) + '.html'
        # self.textArea.append(url)
        print(add_text(url))