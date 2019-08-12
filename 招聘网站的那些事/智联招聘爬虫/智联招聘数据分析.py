#coding:utf-8
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# 解决matplotlib显示中文问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

client = pymongo.MongoClient('localhost')
db = client['test']
table = db['python_人脸属性相关']
columns = ['zwmc',
           'gsmc',
           'zwyx',
           'gbsj',
           'gzdd',
           'fkl',
           'brief',
           'zw_link',
           '_id',
           'save_date']

df = pd.DataFrame([records for records in table.find()],columns=columns)
print('总行数为：{}行'.format(df.shape[0]))
print(df.head())

df['save_date'] = pd.to_datetime(df['save_date'])
print(df['save_date'].dtype)

#帅选月薪格式为的信息
df_clean = df[['zwmc',
           'gsmc',
           'zwyx',
           'gbsj',
           'gzdd',
           'fkl',
           'brief',
           'zw_link',
           'save_date']]

#对月薪的数据进行筛选

df_clean = df_clean[df_clean['zwyx'].str.contains('\d+-\d+',regex=True)]
print('总行数为：{}行'.format(df_clean.shape[0]))
# df_clean.head()

s_min, s_max = df_clean.loc[: , 'zwyx'].str.split('-',1).str
df_min = pd.DataFrame(s_min)
df_min.columns = ['zwyx_min']
df_max = pd.DataFrame(s_max)
df_max.columns = ['zwyx_max']

df_clean_concat = pd.concat([df_clean, df_min, df_max], axis=1)
# df_clean['zwyx_min'].astype(int)
df_clean_concat['zwyx_min'] = pd.to_numeric(df_clean_concat['zwyx_min'])
df_clean_concat['zwyx_max'] = pd.to_numeric(df_clean_concat['zwyx_max'])
# print(df_clean['zwyx_min'].dtype)
print(df_clean_concat.dtypes)
df_clean_concat.head(2)

#将数据信息按职位月薪进行排序
df_clean_concat.sort_values('zwyx_min',inplace=True)
# df_clean_concat.tail()

