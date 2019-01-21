'''
@Coding: 
@Author: Johnson
@Date: 2019-01-21 13:48:58
@Description: 
@Email: 593956670@qq.com
'''
# -*- coding: utf-8 -*-
#导入所需库
import json
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import squarify
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PatchCollection
 
#获取每条微博评论的url参数
def get_comment_parameter():
    url = 'https://m.weibo.cn/api/container/getIndex?uid=1773294041&luicode=10000011&lfid=100103type%3D1%26q%3D%E7%8E%8B%E8%8F%8A&featurecode=20000320&type=uid&value=1773294041&containerid=1076031773294041'
    c_r = requests.get(url)
     for i in range(2,11):
        c_parameter = (json.loads(c_r.text)["data"]["cards"][i]["mblog"]["id"])
        comment_parameter.append(c_parameter)
    return comment_parameter
 
 
if __name__ == "__main__":
 
    comment_parameter = []#用来存放微博url参数
    comment_url = []#用来存放微博url
    user_id = []#用来存放user_id
    comment = []#用来存放评论
    containerid = []#用来存放containerid
    feature = []#用来存放用户信息
    id_lose = []#用来存放访问不成功的user_id
 
    get_comment_parameter()
 
    #获取每条微博评论url
    c_url_base = 'https://m.weibo.cn/api/comments/show?id='
    for parameter in comment_parameter:
        for page in range(1,101):#提前知道每条微博只可抓取前100页评论
            c_url = c_url_base + str(parameter) + "&page=" + str(page)
            comment_url.append(c_url)
 
    #获取每个url下的user_id以及评论
    for url in comment_url:
        u_c_r = requests.get(url)
        try:
            for m in range(0,9):#提前知道每个url会包含9条用户信息
                one_id = json.loads(u_c_r.text)["data"]["data"][m]["user"]["id"]
                user_id.append(one_id)
                one_comment = json.loads(u_c_r.text)["data"]["data"][m]["text"]
                comment.append(one_comment)
        except:
            pass
 
 
    #获取每个user对应的containerid
    user_base_url = "https://m.weibo.cn/api/container/getIndex?type=uid&value="
    for id in set(user_id):#需要对user_id去重
        containerid_url = user_base_url + str(id)
        try:
            con_r = requests.get(containerid_url)
            one_containerid = json.loads(con_r.text)["data"]['tabsInfo']['tabs'][0]["containerid"]
            containerid.append(one_containerid)
        except:
            containerid.append(0)
 
    #获取每个user_id对应的基本信息
    #这里需要设置cookie和headers模拟请求
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
    headers = {"User-Agent":user_agent}
    m = 1
    for num in zip(user_id,containerid):
        url = "https://m.weibo.cn/api/container/getIndex?uid="+str(num[0])+"&luicode=10000011&lfid=100103type%3D1%26q%3D&featurecode=20000320&type=uid&value="+str(num[0])+"&containerid="+str(num[1])
        try:
            r = requests.get(url,headers = headers,cookies = cookie)
            feature.append(json.loads(r.text)["data"]["cards"][1]["card_group"][1]["item_content"].split("  "))
            print("成功第{}条".format(m))
            m = m + 1
            time.sleep(1)
        except:
            id_lose.append(num[0])
 
    #将featrue建立成DataFrame结构便于后续分析
    user_info = pd.DataFrame(feature,columns = ["性别","年龄","星座","国家城市"])

'''
数据预处理

 

根据用户基本信息的显示顺序，性别、年龄、星座、国家城市，主要用了以下几方面的数据处理逻辑：

 

对于国家列为空，星座列不空且不包含座字，则认为是国家城市名，则把星座列赋值给国家城市列。

对于国家列为空，星座列也为空，年龄列不为空且不包含岁或座字，则把年龄列赋值给国家城市列。

对于星座列为空，但是年龄列包含座字，则把年龄列赋值给星座列。

对于星座列不包含座的，全部赋值为“未知”。

对于年龄列不包含岁的，全部赋值为“999岁”(为便于后续好筛选)。

对于国家列为空的，全部赋值为“其他”。

 
--------------------- 
作者：菜鸟Python笔记 
来源：CSDN 
原文：https://blog.csdn.net/qq_41888542/article/details/81143170 
版权声明：本文为博主原创文章，转载请附上博文链接！
'''

'''
分析模块
'''
#数据清洗
user_info1 = user_info[(user_info["性别"] == "男") | (user_info["性别"] == "女")]#去除掉性别不为男女的部分
user_info1 = user_info1.reindex(range(0,5212))#重置索引
 
 
user_index1 = user_info1[(user_info1["国家城市"].isnull() == True)&(user_info1["星座"].isnull() == False)
                         &(user_info1["星座"].map(lambda s:str(s).find("座")) == -1)].index
for index in user_index1:
    user_info1.iloc[index,3] = user_info1.iloc[index,2]
 
user_index2 = user_info1[((user_info1["国家城市"].isnull() == True)&(user_info1["星座"].isnull() == True)
                          &(user_info1["年龄"].isnull() == False)&(user_info1["年龄"].map(lambda s:str(s).find("岁")) == -1))].index
for index in user_index2:
    user_info1.iloc[index,3] = user_info1.iloc[index,1]
 
user_index3 = user_info1[((user_info1["星座"].map(lambda s:str(s).find("座")) == -1)&
                          (user_info1["年龄"].map(lambda s:str(s).find("座")) != -1))].index
for index in user_index3:
    user_info1.iloc[index,2] = user_info1.iloc[index,1]
 
user_index4 = user_info1[(user_info1["星座"].map(lambda s:str(s).find("座")) == -1)].index
for index in user_index4:
    user_info1.iloc[index,2] = "未知"
 
user_index5 = user_info1[(user_info1["年龄"].map(lambda s:str(s).find("岁")) == -1)].index
for index in user_index5:
    user_info1.iloc[index,1] = "999岁"
 
user_index6 = user_info1[(user_info1["国家城市"].isnull() == True)].index
for index in user_index6:
    user_info1.iloc[index,3] = "其他"




