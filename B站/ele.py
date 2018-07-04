#coding:utf-8

import requests
import json
from multiprocessing.dummy import Pool as ThreadPool
import sys
import time
import random


def datetime_to_timestamp_in_milliseconds(d):
    current_milli_time = lambda: int(round(time.time() * 1000))
    return current_milli_time()


reload(sys)

sys.setdefaultencoding('utf-8')

urls = []

head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}

offset = random.randint(0, 200)

latitude = 23.2022279780  # 请改为自己的经纬度
longitude = 113.3687505327  # 请改为自己的经纬度
url = 'https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash=ws0e6hvhnh0&latitude=' + str(
    latitude) + '&limit=24&longitude=' + str(longitude) + '&offset=' + str(
    offset) + '&terminal=web'
urls.append(url)


def getsource(url):
    jscontent = requests.get(url, headers=head).content
    data = json.loads(jscontent)
    if data:
        id = random.randint(0, 23)
        shop_name = data[id]['name']
        shop_id = data[id]['id']
        shop_content = requests.get('https://www.ele.me/restapi/shopping/v2/menu?restaurant_id=' + str(shop_id),
                                    headers=head).content
        shop_data = json.loads(shop_content)
        food_id = random.randint(0, len(shop_data[0]['foods']) - 1)
        food_name = shop_data[0]['foods'][food_id]['name']
        print u'亲爱的小主，奴婢今天晚上为您推荐的菜式是：'
        print food_name + '\n'
        print u'这道菜售价为 ' + str(shop_data[0]['foods'][food_id]['specfoods'][0]['price']) + u' 元'
        print u'本月共售出 ' + str(shop_data[0]['foods'][food_id]['month_sales']) + u' 份'
        print u'共有 ' + str(shop_data[0]['foods'][food_id]['rating_count']) + u' 个人评价，评价得分 ' + str(
            shop_data[0]['foods'][food_id][
                'rating']) + u' 颗星'
        print u'该菜式来自：' + shop_name

        print u'该店的配送费是：' + data[id]['piecewise_agent_fee']['description'].replace(u'配送费', '') + '\n'

        print u'如果下单，您需要支付：' + str(
            shop_data[0]['foods'][food_id]['specfoods'][0]['price'] + data[id]['piecewise_agent_fee']['rules'][0][
                'fee']) + u' 元 _(:3」∠)_'
        print u'如果您喜欢这道菜，可以点击：' + 'https://www.ele.me/shop/' + str(shop_id) + u' 下单购买 (๑´ڡ`๑)'


pool = ThreadPool(1)
try:
    results = pool.map(getsource, urls)
except Exception:
    print 'ConnectionError'
    time.sleep(5)
    results = pool.map(getsource, urls)

pool.close()
pool.join()
