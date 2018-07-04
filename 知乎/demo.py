#coding:gbk
import numpy as np
import pandas as pd
import pymongo
from datetime import datetime
# from urllib.parse import urlencode
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import time
from itertools import product
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
from pprint import pprint
import csv
import requests
from collections import Counter
import jieba
# from wordcound import WordCloud
import os
import json
import csv
from pprint import pprint
import requests
import xlwt
import threading
# from functools import namedtuple
from concurrent import futures
import time

headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/56.0.2924.87 Safari/537.36',
}

# 专栏信息 API
url = 'https://zhuanlan.zhihu.com/api/columns/passer/posts?limit=100&'
req = requests.get(url, headers=headers).json()

result = []
headers = ('作者', '作者首页', '文章标题', '文章地址', '发布时间', '赞同数', '评论数')

for r in req:
    author = r['author']['name']                        # 作者
    author_url = r['author']['profileUrl']              # 作者首页
    title = r['title']                                  # 文章标题
    url = 'https://zhuanlan.zhihu.com' + r['url']       # 文章地址
    post_time = r['publishedTime']                      # 发布时间
    likes = r['likesCount']                             # 赞同数
    comments = r['commentsCount']                       # 评论数
    result.append((author, author_url, title, url, post_time, likes, comments))

pprint(result)


