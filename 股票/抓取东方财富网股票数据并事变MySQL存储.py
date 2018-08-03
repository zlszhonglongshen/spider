# 导入需要使用到的模块
import urllib
import re
import pandas as pd
import pymysql
import os
import time
import csv


# # 爬虫抓取网页函数
# def getHtml(url):
#     html = urllib.request.urlopen(url).read()
#     html = html.decode('gbk')
#     return html
#
#
# # 抓取网页股票代码函数
# def getStackCode(html):
#     s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
#     pat = re.compile(s)
#     code = pat.findall(html)
#     return code
#
#
# #########################开始干活############################
# Url = 'http://quote.eastmoney.com/stocklist.html'  # 东方财富网股票数据连接地址
filepath = './data/'  # 定义数据文件保存路径
# # 实施抓取
# code = getStackCode(getHtml(Url))
# # 获取所有股票代码（以6开头的，应该是沪市数据）集合
# CodeList = []
# for item in code:
#     if item[0] == '6':
#         CodeList.append(item)
# num = 0
# # 抓取数据并保存到本地csv文件
# for code in CodeList:
#     print('正在获取股票%s数据' % code)
#     url = 'http://quotes.money.163.com/service/chddata.html?code=0' + code + \
#           '&end=20180801&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
#     num += 1
#     print('正在获得第{}只股票数据！！！'.format(num))
#     urllib.request.urlretrieve(url, filepath + code + '.csv')
#     time.sleep(5)

# ##########################将股票数据存入数据库###########################

# 数据库名称和密码
name = 'mysql'
password = 'Infinitus_2018'  # 替换为自己的账户名和密码
# 建立本地数据库连接(需要先开启数据库服务)
db = pymysql.connect('172.20.71.35', name, password, charset='gbk')
cursor = db.cursor()
# 创建数据库stockDataBase
# sqlSentence1 = "create database stockDataBase"
# cursor.execute(sqlSentence1)  # 选择使用当前数据库
sqlSentence2 = "use stockDataBase;"
cursor.execute(sqlSentence2)

# 获取本地文件列表
fileList = os.listdir(filepath)
# 依次对每个数据文件进行存储
for fileName in fileList:
    with open(filepath + fileName,"r",encoding='gbk') as f:
        data = csv.reader(f)
        # 创建数据表，如果数据表已经存在，会跳过继续执行下面的步骤print('创建数据表stock_%s'% fileName[0:6])
        sqlSentence3 = "create table stock_%s" % fileName[0:6] + "(日期 VARCHAR(20), 股票代码 VARCHAR(10),     名称 VARCHAR(10),\
                           收盘价 VARCHAR(20),    最高价    VARCHAR(20), 最低价 VARCHAR(20), 开盘价 VARCHAR(20), 前收盘 VARCHAR(20), 涨跌额    VARCHAR(20), \
                           涨跌幅 VARCHAR(20), 换手率 VARCHAR(20), 成交量 VARCHAR(20), 成交金额 VARCHAR(20), 总市值 VARCHAR(20), 流通市值 VARCHAR(20))"
        cursor.execute(sqlSentence3)
        print('数据表已存在！')

        # 迭代读取表中每行数据，依次存储（整表存储还没尝试过）
        print('正在存储stock_%s' % fileName[0:6])
        # for i in range(0, length):
        #     record = tuple(data.loc[i])
        for row in data:
            record = (row[0], row[1], row[2],row[3], row[4], row[5],row[6], row[7], row[8],row[9], row[10], row[11],row[12], row[13], row[14])
            # 插入数据语句

            sqlSentence4 = "insert into stock_%s" % fileName[0:6] + "(日期, 股票代码, 名称, 收盘价, 最高价, 最低价, 开盘价, 前收盘, 涨跌额, 涨跌幅, 换手率, 成交量, 成交金额, 总市值, 流通市值) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # 获取的表中数据很乱，包含缺失值、Nnone、none等，插入数据库需要处理成空值
            sqlSentence4 = sqlSentence4.replace('nan', 'null').replace('None', 'null').replace('none', 'null')
            cursor.execute(sqlSentence4,record)

# 关闭游标，提交，关闭数据库连接
cursor.close()
db.commit()
db.close()

# ###########################查询刚才操作的成果##################################
#
# # 重新建立数据库连接
# db = pymysql.connect('localhost', name, password, 'stockDataBase')
# cursor = db.cursor()
# # 查询数据库并打印内容
# cursor.execute('select * from stock_600000')
# results = cursor.fetchall()
# for row in results:
#     print(row)
# # 关闭
# cursor.close()
# db.commit()
# db.close()