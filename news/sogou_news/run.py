# -*- coding: utf-8 -*-
"""
Created on 2019-01-24 13:23
@author: Johnson
Email:593956670@qq.com
@software: PyCharm
"""
import setting as st 
from sogou_news import SogouNews


'''
程序入口
请在setting中国呢传入参数，运行此文件
'''
if st.DATA_FROM=="sogou_news":
    spider = SogouNews()
    spider.crawl_sogou_news()
else:
    print("请指定数据来源...")