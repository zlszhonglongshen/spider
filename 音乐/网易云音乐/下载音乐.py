# -*- coding: utf-8 -*-
import re
import urllib
import urllib2
import os
import stat
import itertools
import re
import sys
import requests
import json
import time
import socket
import urlparse
import csv
import random
from datetime import datetime, timedelta
import lxml.html

from zipfile import ZipFile
from StringIO import StringIO
from downloader import Downloader
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
from itertools import product
import sys
reload(sys)
sys.setdefaultencoding('utf8')
URL = 'http://music.163.com'
NUM = 5
def download(url, user_agent='wswp', num_try=2):

    headers = {'User_agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error', e.reason
        html = None
        if num_try > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, user_agent, num_try - 1)
    return html


def get_song_list(url):
    html = download(url)
    res = r'<ul class="f-hide">(.*?)</ul>'
    mm = re.findall(res,html,re.S | re.M)
    #print mm
    res = r'<li><a .*?>(.*?)</a></li>'
    song_list = re.findall(res, html,re.S | re.M)
    return song_list

#获取网易云歌单 eg:/playlist?id=706469943
def get_play_list(html):
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all(name='a', attrs={'class': 'tit f-thide s-fc0'})
    list = []
    for each in results:
        ee = each.get('href')
        list.append(ee)
    return list

def download_music(url, song_name):
    print "Downloading song_name:" + song_name
    path = "songs"
    if not os.path.isdir(path):
        os.mkdir(path)
    f = open(path + '/' + song_name + '.flac', 'wb')
    f.write(download(url))
    f.close()

def download_song(song_name,singer):

    url = "http://sug.music.baidu.com/info/suggestion"
    #百度音乐搜索获得songid
    mess = song_name + singer
    payload = {'word': mess, 'version': '2.1.1', 'from': '0'}
    r = requests.get(url, params=payload)
    contents = r.text
    d = json.loads(contents, encoding="utf-8")
    #print d
    if ('data' not in d):
        print "do not have flac"
        return 0
    if ('song' not in d["data"]):
        print "do not have flac"
        return 0
    song_id = d["data"]["song"][0]["songid"]

    print "song_id:"+song_id

    url = "http://music.baidu.com/data/music/fmlink" #百度音乐免费api接口
    '''
        http://music.baidu.com/data/music/fmlink?rate=320&songIds=242078437&type=&callback=cb_download&_t=1468380564513&format=json
    '''
    payload = {'songIds': song_id, 'type': 'mp3'}
    r = requests.get(url, params=payload)
    contents = r.text
    try:
        d = json.loads(contents, encoding="utf-8")
    except:
        return 0
    if d is not None and 'data' not in d or d['data'] == '':
        return 0
    songlink = d["data"]["songList"][0]["songLink"]
    if (len(songlink) < 10):
        print "do not have flac"
        return 0
    print "Song Source: " + songlink
    download_music(songlink,mess)

def get_song_singer(url):
    html = download(url)
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all(name='textarea', attrs={'style': 'display:none;'})
    mess = str(results[0])
    tt = len('<textarea style="display:none;">')
    result = mess[tt:]
    tt = len('</textarea>)')-1
    resu = result[:-tt]
    list = json.loads(resu, encoding="utf-8")
    singer_list = []
    for each in list:
        singer_list.append(each["artists"][0]["name"])
    return singer_list



if __name__ == '__main__':

    num = 0
    for flag in range(1,5):
        if flag > 1:
            page = (flag - 1) * 35
            url = 'http://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset='+str(page)
        else:
            url = 'http://music.163.com/discover/playlist'
        print url
        html = download(url)
        list = get_play_list(html)
        for i in list:
            song_list_url = URL + i
            print song_list_url
            singer_list = get_song_list(song_list_url)
            singer_name = get_song_singer(song_list_url)
            tt = len(singer_list)
            mm = len(singer_name)
            index = min(tt,mm)
            num = num + mm
            for j in range(0, index):
                print singer_name[j]
                print singer_list[j]
                download_song(singer_list[j],singer_name[j])
                print "\n"

    print "Download " + str(num) + " music\n"