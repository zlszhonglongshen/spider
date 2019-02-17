# -*- coding: utf-8 -*-
"""
Created on 2019/2/17 23:17
@author: Johnson
Email:593956670@qq.com
@software: PyCharm
"""
from get_index_information import BaiduIndex
import pandas as pd

if __name__ == "__main__":
    """
    最多一次请求5个关键词
    """

    # baidu_index = BaiduIndex("无限极", '2018-12-13', '2019-02-15', 0)
    #
    # 无限极 = pd.DataFrame()
    #
    # for data in baidu_index('无限极', 'all'):
    #     temp = pd.DataFrame(pd.Series(data)).T
    #     无限极 = pd.concat([无限极, temp])
    #
    # # 无限极.index = range(len(无限极.shape))
    # print(无限极)

    Df = pd.DataFrame()
    starttime = '2018-12-13'
    endtime = '2019-02-15'
    for i in ["无限极", "传销", "保健品", "权健"]:
        baidu_index = BaiduIndex(i, starttime,endtime, 0)
        Temp = pd.DataFrame()
        for data in baidu_index(i, 'all'):
            temp = pd.DataFrame(pd.Series(data)).T
            Temp = pd.concat([Temp, temp])
        Temp['keyword'] = [i]*(Temp.shape[0])
        Df = pd.concat([Df,Temp])
    print(Df)
    # Df.to_csv("e:/Df.csv",encoding="gbk")



    # # 获取全部5个关键词的全部数据
    # print(baidu_index.result)
    # # 获取1个关键词的全部数据
    # print(baidu_index.result['无限极'])
    # # 获取1个关键词的移动端数据
    # print(baidu_index.result['无限极']['wise'])
    # # 获取1个关键词的pc端数据
    # print(baidu_index.result['无限极']['pc'])