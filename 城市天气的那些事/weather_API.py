# -*- coding: utf-8 -*-
"""
Created on 2019/1/11 20:21
@Author: Johnson
@Email:593956670@qq.com
@File: weather_API.py
"""


'''
不能用
'''
import json,urllib
from urllib import urlencode

def main():
    appkey = "274debb981f8f7c7f948b70099af4a77"
    request1(appkey, "GET")

#根据城市查询天气
def request1(appkey,m='GET'):
    url = "http://op.juhe.cn/onebox/weather/query"
    params = {"cityname": "广州",  # 要查询的城市，如：温州、上海、北京
    "key": appkey,  # 应用APPKEY(应用详细页查询)
    "dtype": "",  # 返回数据的格式,xml或json，默认json 
    }

    params = urlencode(params)
    if m=='GET':
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url,params)
    content = f.read()
    res = json.loads(content.decode('utf-8'))
    if res:
        error_code = res['error_code']
        if error_code==0:
            print(res['result'])
        else:
            print("%s:%s" % (res["error_code"],res["reason"]))
    else:
        print("request api error")

if __name__ == '__main__':
    main()