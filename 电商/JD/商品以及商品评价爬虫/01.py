# -*- coding: utf-8 -*-
"""
Created on 2018/9/16 15:11
@author: Johnson
"""
import requests
import re
import pymongo
import threading
import json

"""
查询商品id
"""
def find_product_id(key_word):
    jd_url = 'https://search.jd.com/Search'
    product_ids = []
    #爬前3页
    for i in range(1,3):
        param = {'keyword':key_word,'enc':'utf-8','page':i}
        response = requests.get(jd_url,params=param)
        #商品id
        ids = re.findall('data-pid="(.*?)"',response.text,re.S)
        product_ids+=ids
    return product_ids

'''
接下来就是爬取评论数据，通过preview发现获取用户评价这个请求相应的格式是一个字符串后面拼接了一个json
'''

"""
获取评论内容
"""
def get_comment_message(product_id):
    urls = ['https://sclub.jd.com/comment/productPageComments.action?' \
            'callback=fetchJSON_comment98vv53282&' \
            'productId={}' \
            '&score=0&sortType=5&' \
            'page={}' \
            '&pageSize=10&isShadowSku=0&rid=0&fold=1'.format(product_id, page) for page in range(1, 11)]
    for url in urls:
        response = requests.get(url)
        html = response.text
        #删除无用字符
        html = html.replace('fetchJSON_comment98vv53282(', '').replace(');', '')
        data = json.loads(html)
        comments = data['comments']
        t = threading.Thread(target=save_mongo,args=(comments,))
        t.start()


#mongo服务
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
# jd数据库
db = client.jd
# product表,没有自动创建
product_db = db.product

#保存mongo
def save_mongo(comments):
    for comment in comments:
        product_data = {}
        #颜色
        #flush_data清洗数据的方法
        product_data['product_color'] = flush_data(comment['productColor'])
        # size
        product_data['product_size'] = flush_data(comment['productSize'])
        # 评论内容
        product_data['comment_content'] = comment['content']
        # create_time
        product_data['create_time'] = comment['creationTime']
        # 插入mongo
        product_db.insert(product_data)

#因为每种商品的颜色，尺寸描述上有差异，为了方面统计
def flush_data(data):
    if '肤' in data:
        return '肤色'
    if '黑' in data:
        return '黑色'
    if '紫' in data:
        return '紫色'
    if '粉' in data:
        return '粉色'
    if '蓝' in data:
        return '蓝色'
    if '白' in data:
        return '白色'
    if '灰' in data:
        return '灰色'
    if '槟' in data:
        return '香槟色'
    if '琥' in data:
        return '琥珀色'
    if '红' in data:
        return '红色'
    if '紫' in data:
        return '紫色'
    if 'A' in data:
        return 'A'
    if 'B' in data:
        return 'B'
    if 'C' in data:
        return 'C'
    if 'D' in data:
        return 'D'


#创建一个线程锁
lock = threading.Lock()
#获取评论线程
def spider_jd(ids):
    while ids:
        #加锁
        lock.acquire()
        #取出第一个元素
        id = ids[0]
        #将取出的元素从列表中删除，避免重复加载
        del ids[0]
        #释放锁
        lock.release()
        #获取评论内容
        get_comment_message(id)

product_ids = find_product_id("胸罩")
for i in (1,5):
    #增加一个获取评论的县城
    t = threading.Thread(target=spider_jd,args=(product_ids,))
    #启动线程
    t.start()








