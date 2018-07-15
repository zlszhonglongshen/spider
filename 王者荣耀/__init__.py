#coding:utf-8

"""
百度“王者荣耀”进入官网，进入https://pvp.qq.com/，按F12进入调试界面，然后按F5刷新界面，
图中标识的herolist.json文件就是我们所需要的英雄列表，其中包括英雄编号、英雄名称、英雄类型、皮肤的名称等信息，
在文件上右击复制链接http://pvp.qq.com/web201605/js/herolist.json

"""
import urllib.request
import json
import os
import time
import pymysql

response = urllib.request.urlopen("http://pvp.qq.com/web201605/js/herolist.json")

hero_json = json.loads(str(response.read()))
hero_num = len(hero_json)

print(hero_json)
print("hero_num : " , str(hero_num))

# """
# 点击首页的“游戏资料”标签页，进入新的界面后点击一个英雄头像进入英雄资料界面，此处我们以孙尚香为例：
# 同样F12然后F5，将鼠标在孙尚香几个皮肤上依次扫过，来看看调试窗口
# """
#
# # 代码片段2
# hero_name = hero_json[0]['cname']
# skin_names = hero_json[0]['skin_name'].split('|')
# skin_num = len(skin_names)
#
# print('hero_name: ', hero_name)
# print('skin_names :', skin_names)
# print('skin_num: ' + str(skin_num))
#
# #文件夹不存在则创建
# save_dir = 'd:/hearskin/'
# if not os.path.exists(save_dir):
#     os.mkdir(save_dir)
#
# ###下载文件
# for i in range(hero_num):
#     #获取英雄皮肤列表
#     skin_names = hero_json[i]['skin_name'].split('|')
#     for cnt in range(len(skin_names)):
#         save_file_name = save_dir + str(hero_json[i]['ename']) + '-' + hero_json[i]['cname'] + '-' + skin_names[
#             cnt] + '.jpg'
#         skin_url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/' + str(
#             hero_json[i]['ename']) + '/' + str(hero_json[i]['ename']) + '-bigskin-' + str(cnt + 1) + '.jpg'
#
#         if not os.path.exists(save_file_name):
#             urllib.request.urlretrieve(skin_url, save_file_name)
#
#     # 作者：瑶曳风尘
#     # 链接：https: // www.jianshu.com / p / 925
#     # a6070707f
#     # 來源：简书
#     # 简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。
#     #
#
# def Dbinsert():
#     Strtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#     try:
#         db = pymysql.connect(host="localhost",
#                                port=3306,
#                                user="root",
#                                passwd="",
#                                db="mysql",
#                                charset="utf8")
#     except Exception as e:
#         print("数据库连接失败",e)
#
#     #使用cursor（）方法获取操作游标
#     try:
#         cursor = db.cursor()
#     except Exception:
#         print("获取游标异常",Exception)
#     sql = """INSERT INTO WZRY(id,name,skinname,skinurl,time) VALUES (%s,%s,%s,%s,%s) """
#     try:
#         #执行语句
#         print("Start insert...")
#         # print(sql)
#         # print(db.cursor())
#         cursor.execute(sql,[str(hero_json[i]['ename']),hero_json[i]['cname'],skin_name[cnt],skin_url,Strtime])
#     except Exception as e:
#         print("执行SQL语句异常：",e)
#         db.commit()
#         print("Finish.")
#     except Exception:
#         #如果发生错误则回滚
#         db.rollback()
#         #关闭数据库连接
#         db.close()
