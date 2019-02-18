# -*- coding: utf-8 -*-
"""
Created on 2019/2/15 16:28
@Author: Johnson
@Email:593956670@qq.com
@File: demo.py
"""
from get_index import BaiduIndex
import pandas as pd

if __name__ == "__main__":
    """
    最多一次请求5个关键词
    """
    # 查看城市和省份的对应代码
    # print(BaiduIndex.city_code)
    # print(BaiduIndex.province_code)

    baidu_index = BaiduIndex(["无限极","直销", "保健品" ,"权健","华林酸碱平"], '2018-12-13', '2019-02-15',0)


    无限极 = pd.DataFrame()

    for data in baidu_index('无限极', 'all'):
        temp = pd.DataFrame(pd.Series(data)).T
        无限极 = pd.concat([无限极,temp])

    # 无限极.index = range(len(无限极.shape))
    print(无限极)


    # # 获取全部5个关键词的全部数据
    # print(baidu_index.result)
    # # 获取1个关键词的全部数据
    # print(baidu_index.result['无限极'])
    # # 获取1个关键词的移动端数据
    # print(baidu_index.result['无限极']['wise'])
    # # 获取1个关键词的pc端数据
    # print(baidu_index.result['无限极']['pc'])
