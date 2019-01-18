# -*- coding: utf-8 -*-
"""
Created on 2019/1/18 16:41
@Author: Johnson
@Email:593956670@qq.com
@File: 星座.py
"""
import requests
from lxml.html import etree
import json
import time        # 导入模块

# 星座运势
response = requests.get('https://www.xzw.com/fortune/taurus/')
if not response.status_code == 200:
    print('星座运势请求错误：' + str(response.status_code))
sel =etree.HTML(response.text)
fortune = sel.xpath('//div[@class="c_box"]/div[@class="c_cont"]/p/span/text()')[0]
print(fortune)


