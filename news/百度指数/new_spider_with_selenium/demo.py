# -*- coding: utf-8 -*-
"""
Created on 2019/2/15 16:37
@Author: Johnson
@Email:593956670@qq.com
@File: demo.py
"""
from get_index import BaiduIndex

if __name__ == "__main__":
    """
    最多一次请求5个关键词
    """
    # 查看城市和省份的对应代码
    print(BaiduIndex.city_code)
    print(BaiduIndex.province_code)

    baidu_index = BaiduIndex(['张艺兴', 'lol', '极限挑战', '吃鸡'], '2018-12-25', '2019-02-14',901)
    for data in baidu_index('lol', 'all'):
        print(data)

    # 获取全部5个关键词的全部数据
    print(baidu_index.result)
    # 获取1个关键词的全部数据
    print(baidu_index.result['极限挑战'])
    # 获取1个关键词的移动端数据
    print(baidu_index.result['极限挑战']['wise'])
    # 获取1个关键词的pc端数据
    print(baidu_index.result['极限挑战']['pc'])
