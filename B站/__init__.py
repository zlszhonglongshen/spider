#! /usr/bin/env python_人脸属性相关
# -*- coding:utf-8 -*-

import time
import requests
import sys
from prettytable import PrettyTable
import importlib

# 设置编码方式
importlib.reload(sys)


# 返回爬取的数量
def get_Craw_num():
    print("-----------菜 单--------------")
    i = int(input("请输入爬取视频的起始编号"))
    print("-----------------------------")
    return i


# 爬虫的功能实现
def start_craw(url):
    print("开始爬取，请稍候")
    headers = {}
    x = PrettyTable(['视频编号', '播放量', '弹幕', '回复', '收藏', '硬币', '分享'])
    t = 0
    i = get_Craw_num()
    while (t < 100):
        r = requests.get(url.format(i), headers=headers)
        if r.status_code == 200:
            try:
                j = r.json()['data']
                favorite = j['favorite']
                danmaku = j['danmaku']
                coin = j['coin']
                view = j['view']
                share = j['share']
                reply = j['reply']
                favorite = str(favorite)
                danmaku = str(danmaku) + " "
                coin = str(coin)
                view = str(view)
                share = str(share)
                reply = str(reply)
                av_num = "av" + str(i)
                x.add_row([av_num, view, danmaku, reply, favorite, coin, share])
            except Exception as e:
                pass
        else:
            break
        i += 1
        t += 1
    print (x)
    print("爬取完成")


# main函数
if __name__ == "__main__":
    url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid={}'
    start_craw(url)