#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2017/3/29 9:07
# @Author : Lyrichu
# @Email  : 919987476@qq.com
# @File   : NetCloud_comments_plot.py
'''
@Description:
对抓取来的网易云评论数据进行简单的可视化分析
'''
from NetCloud_spider3 import NetCloudCrawl
import requests
import matplotlib.dates as mdates
from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 防止无法显示中文
import matplotlib.pyplot as plt
from datetime import datetime
import re
import time
import pandas as pd
import codecs
import jieba
from wordcloud import WordCloud
from scipy.misc import imread
from os import path
import os


class NetCloudProcessor(NetCloudCrawl):
    # 读取评论文本数据，返回一个列表，列表的每个元素为一个字典，字典中包含用户id，评论内容等
    def read_comments_file(self, filename):
        list_comments = []  # 评论数据列表
        with open(filename, 'r') as f:
            comments_list = f.readlines()  # 读取文本，按行读取，返回列表
            del comments_list[0]  # 删除首个元素
            comments_list = list(set(comments_list))  # 去除重复数据
            count_ = -1  # 记录评论数
            for comment in comments_list:
                comment = comment.replace("\n", "")  # 去除末尾的换行符
                try:
                    if (re.search(re.compile(r'^\d+?'), comment)):  # 如果以数字开头
                        comment_split = comment.split(' ', 5)  # 以空格分割(默认)
                        comment_dict = {}
                        comment_dict['userID'] = comment_split[0]  # 用户ID
                        comment_dict['nickname'] = comment_split[1]  # 用户昵称
                        comment_dict['avatarUrl'] = comment_split[2]  # 用户头像地址
                        comment_dict['comment_time'] = int(comment_split[3])  # 评论时间
                        comment_dict['likedCount'] = int(comment_split[4])  # 点赞总数
                        comment_dict['comment_content'] = comment_split[5]  # 评论内容
                        list_comments.append(comment_dict)
                        count_ += 1
                    else:
                        list_comments[count_]['comment_content'] += comment  # 将评论追加到上一个字典
                except Exception, e:
                    print(e)
        list_comments.sort(key=lambda x: x['comment_time'])
        print(u"去除重复之后有%d条评论!" % (count_ + 1))
        return (count_ + 1, list_comments)  # 返回评论总数以及处理完的评论内容

    # 将网易云的时间戳转换为年-月-日的日期函数
    # 时间戳需要先除以1000才能得到真实的时间戳
    # format 为要转换的日期格式
    def from_timestamp_to_date(self, time_stamp, format):
        time_stamp = time_stamp * 0.001
        real_date = time.strftime(format, time.localtime(time_stamp))
        return real_date

    # 统计相关数据写入文本文件
    def count_comments_info(self, comments_list, count_, song_name):
        x_date_Ym = []  # 评论数按年月进行统计
        x_date_Ymd = []  # 评论数按年月日进行统计
        x_likedCount = []  # 点赞总数分布
        for i in range(count_):
            time_stamp = comments_list[i]['comment_time']  # 时间戳
            real_date_Ym = self.from_timestamp_to_date(time_stamp, '%Y-%m')  # 按年月进行统计
            real_date_Ymd = self.from_timestamp_to_date(time_stamp, '%Y-%m-%d')  # 按年月日统计
            likedCount = comments_list[i]['likedCount']  # 点赞总数
            x_date_Ym.append(real_date_Ym)
            x_date_Ymd.append(real_date_Ymd)
            x_likedCount.append(likedCount)
        x_date_Ym_no_repeat = []
        y_date_Ym_count = []
        x_date_Ymd_no_repeat = []
        y_date_Ymd_count = []
        x_likedCount_no_repeat = []
        y_likedCount_count = []
        # 年月
        for date_ in x_date_Ym:
            if date_ not in x_date_Ym_no_repeat:
                x_date_Ym_no_repeat.append(date_)
                y_date_Ym_count.append(x_date_Ym.count(date_))
        # 年月日
        for date_ in x_date_Ymd:
            if date_ not in x_date_Ymd_no_repeat:
                x_date_Ymd_no_repeat.append(date_)
                y_date_Ymd_count.append(x_date_Ymd.count(date_))

        for likedCount in x_likedCount:
            if likedCount not in x_likedCount_no_repeat:
                x_likedCount_no_repeat.append(likedCount)
                y_likedCount_count.append(x_likedCount.count(likedCount))
        # 将统计的数据存入txt文件
        with open(u"%s/comments_num_by_Ym.txt" % song_name, "w") as f:
            f.write("date_Ym comments_num\n")
            for index, date_Ym in enumerate(x_date_Ym_no_repeat):
                f.write(x_date_Ym_no_repeat[index] + " " + str(y_date_Ym_count[index]) + "\n")
            print(u"成功写入comments_num_by_Ym.txt!")
        with open(u"%s/comments_num_by_Ymd.txt" % song_name, "w") as f:
            f.write("date_Ymd comments_num\n")
            for index, date_Ymd in enumerate(x_date_Ymd_no_repeat):
                f.write(x_date_Ymd_no_repeat[index] + " " + str(y_date_Ymd_count[index]) + "\n")
            print(u"成功写入comments_num_by_Ymd.txt!")
        with open(u"%s/likedCount.txt" % song_name, "w") as f:
            f.write("likedCount count_num\n")
            for index, likedCount in enumerate(x_likedCount_no_repeat):
                f.write(str(x_likedCount_no_repeat[index]) + " " + str(y_likedCount_count[index]) + "\n")
            print(u"成功写入likedCount.txt!")

    # 得到处理过的x_date 和 count 统计信息
    def get_xdate_ycount(self, count_file_name, date_type, min_date_Ym, max_date_Ym, min_date_Ymd, max_date_Ymd):
        with open(count_file_name, 'r') as f:
            list_count = f.readlines()
            # comment_or_like = list_count[0].replace("\n","").split(" ")[1] # 判断是评论数还是点赞数
            # song_name = count_file_name.split("/")[0] # 歌曲名字
            del list_count[0]
            x_date = []
            y_count = []
            for content in list_count:
                content.replace("\n", "")
                res = content.split(' ')
                if (date_type == '%Y-%m-%d'):
                    if (int("".join(res[0].split("-"))) >= int("".join(min_date_Ymd.split("-"))) and int(
                            "".join(res[0].split("-"))) <= int("".join(max_date_Ymd.split("-")))):
                        x_date.append(res[0])
                        y_count.append(int(res[1]))
                else:
                    if (int("".join(res[0].split("-"))) >= int("".join(min_date_Ym.split("-"))) and int(
                            "".join(res[0].split("-"))) <= int("".join(max_date_Ym.split("-")))):
                        x_date.append(res[0])
                        y_count.append(int(res[1]))
        return (x_date, y_count)

    # 绘制图形展示歌曲评论以及点赞分布
    # plot_type:为 'plot' 绘制散点图   为 'bar' 绘制条形图
    # date_type 为日期类型
    # time_distance 为时间间隔(必填)例如:5D 表示5天,1M 表示一个月
    # min_liked_num 为绘图时的最小点赞数
    # max_liked_num 为绘图时的最大点赞数
    # min_date_Ym 为最小日期(年-月形式)
    # max_date_Ym 为最大日期(年-月形式)
    # min_date_Ymd 为最小日期(年-月-日形式)
    # max_date_Ymd 为最大日期(年-月-日形式)
    def plot_comments(self, song_name, settings):
        comment_type = settings['comment_type']
        date_type = settings['date_type']
        plot_type = settings['plot_type']
        bar_width = settings['bar_width']
        rotation = settings['rotation']
        time_distance = settings['time_distance']
        min_date_Ymd = settings['min_date_Ymd']
        max_date_Ymd = settings['max_date_Ymd']
        min_date_Ym = settings['min_date_Ym']
        max_date_Ym = settings['max_date_Ym']
        if (comment_type):  # 评论
            if (date_type == '%Y-%m-%d'):
                count_file_name = u"%s/comments_num_by_Ymd.txt" % song_name
            else:
                count_file_name = u"%s/comments_num_by_Ym.txt" % song_name
        else:
            count_file_name = u"%s/likedCount.txt" % song_name
        with open(count_file_name, 'r') as f:
            list_count = f.readlines()
            del list_count[0]
            if (comment_type):  # 如果是评论
                x_date = []
                y_count = []
                for content in list_count:
                    content.replace("\n", "")
                    res = content.split(' ')
                    if (date_type == '%Y-%m-%d'):
                        if (int("".join(res[0].split("-"))) >= int("".join(min_date_Ymd.split("-"))) and int(
                                "".join(res[0].split("-"))) <= int("".join(max_date_Ymd.split("-")))):
                            x_date.append(res[0])
                            y_count.append(int(res[1]))
                    else:
                        if (int("".join(res[0].split("-"))) >= int("".join(min_date_Ym.split("-"))) and int(
                                "".join(res[0].split("-"))) <= int("".join(max_date_Ym.split("-")))):
                            x_date.append(res[0])
                            y_count.append(int(res[1]))
            else:  # 如果是点赞
                # 分为10-100,100-1000,1000-10000,10000以上这5个区间，由于绝大多数歌曲评论点赞数都在10赞一下
                # 超过99%，所以10赞以下暂时忽略
                x_labels = [u'10-100', u'100-1000', u'1000-10000', u'10000以上']
                y_count = [0, 0, 0, 0]
                for content in list_count:
                    content.replace("\n", "")
                    res = content.split(' ')
                    if (int(res[0]) <= 100 and int(res[0]) >= 10):
                        y_count[0] += int(res[1])
                    elif (int(res[0]) <= 1000):
                        y_count[1] += int(res[1])
                    elif (int(res[0]) <= 10000):
                        y_count[2] += int(res[1])
                    else:
                        y_count[3] += int(res[1])
        # 如果是评论
        if (comment_type):
            type_text = u"评论"
            x = [datetime.strptime(d, date_type).date() for d in x_date]
            # 配置横坐标为日期类型
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%s' % date_type))
            if (date_type == '%Y-%m-%d'):
                plt.gca().xaxis.set_major_locator(mdates.DayLocator())
            else:
                plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
            if (plot_type == 'plot'):
                plt.plot(x, y_count, color=settings['color'])
            elif (plot_type == 'bar'):
                plt.bar(x, y_count, width=bar_width, color=settings['color'])
            else:
                plt.scatter(x, y_count, color=settings['color'])
            plt.gcf().autofmt_xdate(rotation=rotation)  # 自动旋转日期标记
            plt.title(u"网易云音乐歌曲《" + song_name + u"》" + type_text + u"数目分布")
            plt.xlabel(u"日期")
            plt.ylabel(u"数目")
            plt.xticks(pd.date_range(x[0], x[-1], freq="%s" % time_distance))  # 设置日期间隔
            plt.show()
        else:  # 如果是点赞
            x = y_count
            type_text = u"点赞"
            pie_colors = settings['pie_colors']
            auto_pct = settings['auto_pct']  # 百分比保留几位小数
            expl = settings['expl']  # 每块距离圆心的距离
            plt.pie(x, labels=x_labels, explode=expl, colors=pie_colors, autopct=auto_pct)
            plt.title(u"网易云音乐歌曲《" + song_name + u"》" + type_text + u"数目分布")
            plt.legend(x_labels)
            plt.show()
        plt.close()

    # 生成某个歌曲的统计信息文件
    def generate_count_info_files(self, song_name):
        filename = "%s/%s.txt" % (song_name, song_name)
        count_, list_comments = self.read_comments_file(filename)
        print(u"%s有%d条评论!" % (song_name, count_))
        self.count_comments_info(list_comments, count_, song_name)

    # 一步完成数据抓取，生成统计信息文件的工作
    def create_all_necessary_files(self, song_id, song_name):
        start_time = time.time()
        # 数据抓取并写入文件
        self.save_all_comments_to_file(song_id, song_name)
        # 生成热门评论文件
        url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_%d/?csrf_token=" % song_id
        hot_comments_list = self.get_hot_comments(url)
        self.save_to_file(hot_comments_list, u"%s/hotcomments.txt" % song_name)
        # 生成统计信息文件(3个)
        self.generate_count_info_files(song_name)
        # 生成所有评论者信息文件
        self.save_commenters_info_to_file(song_name)
        # 生成 评论词云(全部评论)
        self.draw_wordcloud(song_name, singer_name=False)
        end_time = time.time()
        print(u"任务完成!程序耗时%f秒!" % (end_time - start_time))

    # 得到某首歌曲下所有评论者(需要去除重复)的主页信息
    def get_commenters_info(self, filename):
        commenters_info_list = []  # 存放评论用户信息
        with codecs.open(filename, "r", encoding='utf-8') as f:
            lists = f.readlines()
            del lists[0]  # 删除第一行
            commenters_urls_list = []  # 评论者列表
            for info in lists:
                if (re.match(r'^\d.*?', info)):
                    commenters_urls_list.append(u"http://music.163.com/user/home?id=" + info.split(" ")[0])  # 评论者主页地址
            commenters_urls_list = list(set(commenters_urls_list))  # 去除重复的人
            print("共有%d个不同评论者!" % len(commenters_urls_list))
        for index, url in enumerate(commenters_urls_list):
            try:
                info_dict = {}  # 评论用户个人信息字典
                user_id_compile = re.compile(r'.*id=(\d+)')
                user_id = re.search(user_id_compile, url).group(1)
                html = requests.get(url, headers=self.headers).text
                event_count_compile = re.compile(r'<strong id="event_count">(\d+?)</strong>')
                event_count = re.search(event_count_compile, html).group(1)  # 个人动态数目
                follow_count_compile = re.compile(r'<strong id="follow_count">(\d+?)</strong>')
                follow_count = re.search(follow_count_compile, html).group(1)  # 关注人数
                fan_count_compile = re.compile(r'<strong id="fan_count">(\d+?)</strong>')
                fan_count = re.search(fan_count_compile, html).group(1)
                location_compile = re.compile(u'<span>所在地区：(.+?)</span>')  # 注意需要使用unicode编码，正则表达式才能匹配
                location_res = re.search(location_compile, html)
                if (location_res):
                    location = location_res.group(1)
                else:
                    location = u"未知地区"
                self_description_compile = re.compile(u'<div class="inf s-fc3 f-brk">个人介绍：(.*?)</div>')
                if (re.search(self_description_compile, html)):  # 如果可以匹配到
                    self_description = re.search(self_description_compile, html).group(1)
                else:
                    self_description = u"未知个人介绍"
                age_compile = re.compile(r'<span.*?data-age="(\d+)">')
                if (re.search(age_compile, html)):
                    age_time = re.search(age_compile, html).group(1)  # 这个得到的是出生日期距离unix时间戳起点的距离
                    # 需要将其转换为年龄
                    age = (2017 - 1970) - (int(age_time) / (1000 * 365 * 24 * 3600))  # 真实的年龄
                else:
                    age = u"未知年龄"
                listening_songs_num_compile = re.compile(u'<h4>累积听歌(\d+?)首</h4>')
                if (re.search(listening_songs_num_compile, html)):
                    listening_songs_num = re.search(listening_songs_num_compile, html).group(1)  # 听歌总数
                else:
                    listening_songs_num = u'未知听歌总数'
                info_dict['user_id'] = user_id
                info_dict['event_count'] = event_count  # 动态总数
                info_dict['follow_count'] = follow_count  # 关注总数
                info_dict['fan_count'] = fan_count  # 粉丝总数
                info_dict['location'] = location  # 所在地区
                info_dict['self_description'] = self_description  # 个人介绍
                info_dict['age'] = age  # 年龄
                info_dict['listening_songs_num'] = listening_songs_num  # 累计听歌总数
                commenters_info_list.append(info_dict)
                print("成功添加%d个用户信息!" % (index + 1))
            except Exception, e:
                print e
        return commenters_info_list  # 返回评论者用户信息列表

    # 保存评论者的信息
    def save_commenters_info_to_file(self, song_or_singer_name):
        if (os.path.exists(u"%s/%s.txt" % (song_or_singer_name, song_or_singer_name))):
            filename = u"%s/%s.txt" % (song_or_singer_name, song_or_singer_name)
        else:
            filename = u"%s/hotcomments.txt" % song_or_singer_name
        commenters_info_lists = self.get_commenters_info(filename)  # 得到用户信息列表
        with codecs.open(u"%s/commenters_info.txt" % song_or_singer_name, "w", encoding='utf-8') as f:
            f.write(u"用户ID 动态总数 关注总数 粉丝总数 所在地区 个人介绍 年龄 累计听歌总数\n")
            for info in commenters_info_lists:
                user_id = info['user_id']  # 用户id
                event_count = info['event_count']  # 动态数目
                follow_count = info['follow_count']  # 关注的人数
                fan_count = info['fan_count']  # 粉丝数
                location = info['location']  # 所在地区
                self_description = info['self_description']  # 个人介绍
                age = unicode(info['age'])  # 年龄
                listening_songs_num = info['listening_songs_num']  # 累计听歌总数
                full_info = unicode(
                    user_id) + u" " + event_count + u" " + follow_count + u" " + fan_count + u" " + location + u" " + self_description + u" " + age + u" " + listening_songs_num + u"\n"
                f.write(full_info)
        print(u"成功写入文件%s/commenters_info.txt" % song_or_singer_name)

    # 得到某个歌手全部热门歌曲id列表
    def get_songs_ids(self, singer_url):
        ids_list = []
        html = requests.get(singer_url, headers=self.headers, proxies=self.proxies).text
        re_pattern = re.compile(r'<a href="/song\?id=(\d+?)">.*?</a>')
        ids = re.findall(re_pattern, html)
        for id in ids:
            ids_list.append(id)
        return ids_list

    # 得到某个歌手所有歌曲的热门评论
    def get_singer_all_hot_comments(self, singer_name, singer_id):
        singer_url = 'http://music.163.com/artist?id=%d' % singer_id
        song_ids = self.get_songs_ids(singer_url)  # 得到歌手所有热门歌曲id列表
        for song_id in song_ids:
            url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_%d/?csrf_token=" % int(song_id)
            hot_comments_list = self.get_hot_comments(url)
            if (os.path.exists(singer_name)):
                self.save_to_file(hot_comments_list, u"%s/hotcomments.txt" % singer_name)
            else:
                os.mkdir(singer_name)
                self.save_to_file(hot_comments_list, u"%s/hotcomments.txt" % singer_name)
        print(u"成功写入%s的%d首歌曲!" % (singer_name, len(song_ids)))

    # 在一张图中绘制多个歌曲的评论分布
    # song_names_list 为多个歌曲名字的列表
    # settings 为含有字典元素的列表，每个字典含有每个子图的配置项
    def sub_plot_comments(self, song_names_list, settings, row, col):
        n = len(song_names_list)  # 歌曲总数
        row = row
        col = col
        for i in range(n):
            plt.subplot(row, col, i + 1)
            if (settings[i]['date_type'] == '%Y-%m-%d'):
                count_file_name = u"%s/comments_num_by_Ymd.txt" % song_names_list[i]
            else:
                count_file_name = u"%s/comments_num_by_Ym.txt" % song_names_list[i]
            date_type = settings[i]['date_type']
            min_date_Ym = settings[i]['min_date_Ym']
            max_date_Ym = settings[i]['max_date_Ym']
            min_date_Ymd = settings[i]['min_date_Ymd']
            max_date_Ymd = settings[i]['max_date_Ymd']
            x_date, y_count = self.get_xdate_ycount(count_file_name, min_date_Ym=min_date_Ym, max_date_Ym=max_date_Ym,
                                                    min_date_Ymd=min_date_Ymd, max_date_Ymd=max_date_Ymd,
                                                    date_type=date_type)

            x = [datetime.strptime(d, date_type).date() for d in x_date]
            # 配置横坐标为日期类型
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%s' % date_type))
            if (date_type == '%Y-%m-%d'):
                plt.gca().xaxis.set_major_locator(mdates.DayLocator())
            else:
                plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
            plot_type = settings[i]['plot_type']
            if (plot_type == 'plot'):
                plt.plot(x, y_count, color=settings[i]['color'])
            elif (plot_type == 'bar'):
                plt.bar(x, y_count, width=settings[i]['bar_width'], color=settings[i]['color'])
            else:
                plt.scatter(x, y_count, color=settings[i]['color'])
            plt.gcf().autofmt_xdate(rotation=settings[i]['rotation'])  # 自动旋转日期标记
            plt.title(u"网易云音乐歌曲《" + song_names_list[i] + u"》" + u"评论数目分布(%s到%s)" % (x[0], x[-1]),
                      fontsize=settings[i]['fontsize'])
            plt.xlabel(u"日期")
            plt.ylabel(u"数目")
            plt.xticks(pd.date_range(x[0], x[-1], freq="%s" % settings[i]['time_distance']))  # 设置日期间隔
        plt.subplots_adjust(left=0.2, bottom=0.2, right=0.8, top=0.8, hspace=1.2, wspace=0.3)
        plt.show()

    # 得到评论列表
    def get_comments_list(self, filename):
        with codecs.open(filename, "r", encoding='utf-8') as f:
            lists = f.readlines()
            comments_list = []
            for comment in lists:
                if (re.match(r"^\d.*", comment)):
                    try:
                        comments_list.append(comment.split(" ", 5)[5].replace("\n", ""))
                    except Exception, e:
                        print(e)
                else:
                    comments_list.append(comment)
        return comments_list

    # 绘制词云
    # pic_path 为词云背景图片地址
    # singer_name 为 False 时，则读取歌曲评论文件，否则读取歌手热评文件
    # isFullComments = True 时，读取全部评论，否则只读取热评
    def draw_wordcloud(self, song_name, singer_name, pic_path="JayChou.jpg", isFullComments=True):
        if singer_name == False:
            if isFullComments == True:
                filename = u"%s/%s.txt" % (song_name, song_name)  # 全部评论
            else:
                filename = u"%s/hotcomments.txt" % song_name  # 一首歌的热评
        else:
            filename = u"%s/hotcomments.txt" % singer_name
        comments_list = self.get_comments_list(filename)
        comments_text = "".join(comments_list)
        cut_text = " ".join(jieba.cut(comments_text))  # 将jieba分词得到的关键词用空格连接成为字符串
        d = path.dirname(__file__)  # 当前文件文件夹所在目录
        color_mask = imread(pic_path)  # 读取背景图片
        cloud = WordCloud(font_path=path.join(d, 'simsun.ttc'), background_color='white', mask=color_mask,
                          max_words=2000, max_font_size=40)
        word_cloud = cloud.generate(cut_text)  # 产生词云
        if singer_name == False:
            name = song_name
        else:
            name = singer_name
        word_cloud.to_file(u"%s/%s.jpg" % (name, name))
        print(u"成功生成%s.jpg" % name)

    # 对一首歌曲绘制其某一年某几个月的评论分布
    # date_lists 为要绘制的月份
    def sub_plot_months(self, song_name, DateLists, settings, row, col):
        n = len(DateLists)
        row = row  # 行
        col = col  # 列
        filename = u"%s/comments_num_by_Ymd.txt" % song_name
        date_lists = []
        y_count = []
        with codecs.open(filename, "r", encoding='utf-8') as f:
            lists = f.readlines()
            del lists[0]  # 删除头部信息
            for content in lists:
                date_lists.append(content.split(" ")[0])  # 添加日期信息
                y_count.append(int(content.split(" ")[1]))  # 添加数量信息
        for i in range(n):
            plt.subplot(row, col, i + 1)
            x_date = [date for date in date_lists if re.match(r"%s" % DateLists[i], date)]
            y = [y_count[j] for j in range(len(y_count)) if re.match(r"%s" % DateLists[i], date_lists[j])]
            x = [datetime.strptime(d, "%Y-%m-%d").date() for d in x_date]
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            plot_type = settings[i]['plot_type']
            if (plot_type == 'plot'):
                plt.plot(x, y, color=settings[i]['color'])
            elif (plot_type == 'bar'):
                plt.bar(x, y, width=settings[i]['bar_width'], color=settings[i]['color'])
            else:
                plt.scatter(x, y, color=settings[i]['color'])
            plt.gcf().autofmt_xdate(rotation=settings[i]['rotation'])  # 自动旋转日期标记
            plt.title(u"《%s》%s到%s" % (song_name, x[0], x[-1]), fontsize=settings[i]['fontsize'])
            plt.xlabel(u"日期")
            plt.ylabel(u"评论数目")
            plt.xticks(pd.date_range(x[0], x[-1], freq="%s" % settings[i]['time_distance']))  # 设置日期间隔
        plt.subplots_adjust(left=0.09, bottom=0.27, right=0.89, top=0.83, hspace=0.35, wspace=0.35)
        plt.show()

    # 绘制一首歌曲评论者相关信息的分布
    def sub_plot_commenters_info(self, song_or_singer_name):
        file_name = u"%s/commenters_info.txt" % song_or_singer_name
        with codecs.open(file_name, 'r', encoding='utf-8') as f:
            info_lists = f.readlines()
            del info_lists[0]  # 删除头部信息
            event_count_list = []  # 动态总数
            follow_count_list = []  # 关注总数
            fan_count_list = []  # 粉丝总数
            area_list = []  # 所在地区
            age_list = []  # 年龄
            listen_songs_num_list = []  # 累计听歌数目
            for info in info_lists:
                info.replace("\n", "")
                event_count_list.append(int(info.split(" ")[1]))
                follow_count_list.append(int(info.split(" ")[2]))
                fan_count_list.append(int(info.split(" ")[3]))
                area_res = re.search(re.compile(u'.*\d (.+?-.+?) .*?|.*(未知地区).*'), info)
                if (area_res):
                    if (area_res.group(1)):
                        area_list.append(area_res.group(1))
                age_list.append(info.split(" ")[-2])
                listen_songs_num_list.append(int(info.split(" ")[-1]))
        event_count = [0, 0, 0, 0]
        follow_count = [0, 0, 0, 0, 0]
        fan_count = [0, 0, 0, 0, 0]
        listen_songs_num = [0, 0, 0, 0]
        area_count = [0, 0, 0, 0, 0, 0]
        age_count = [0, 0, 0, 0, 0]
        for content in event_count_list:
            if (content <= 10):
                event_count[0] += 1
            elif (content <= 50):
                event_count[1] += 1
            elif (content <= 100):
                event_count[2] += 1
            else:
                event_count[3] += 1
        for content in follow_count_list:
            if (content < 10):
                follow_count[0] += 1
            elif (content < 30):
                follow_count[1] += 1
            elif (content < 50):
                follow_count[2] += 1
            elif (content < 100):
                follow_count[3] += 1
            else:
                follow_count[4] += 1
        for content in fan_count_list:
            if (content < 10):
                fan_count[0] += 1
            elif (content < 100):
                fan_count[1] += 1
            elif (content < 1000):
                fan_count[2] += 1
            elif (content < 10000):
                fan_count[3] += 1
            else:
                follow_count[4] += 1
        area_no_repeat_list = list(set(area_list))  # 去除重复
        area_tuple = [(area, area_list.count(area)) for area in area_no_repeat_list]
        area_tuple.sort(key=lambda x: x[1], reverse=True)  # 从高到低排列
        for i in range(5):  # 取出排名前4的地区
            area_count[i] = area_tuple[i][1]
        area_count[5] = sum([x[1] for x in area_tuple[5:]])  # 前5名之外的全部地区数量
        area_labels = [x[0] for x in area_tuple[0:5]]  # 前5个地区的名字
        area_labels.append(u"其他地区")
        age_no_repeat_list = list(set(age_list))  # 去除重复
        age_info = [age_list.count(age) for age in age_no_repeat_list]
        for index, age_ in enumerate(age_no_repeat_list):
            if (age_ != u"未知年龄"):  # 排除未知年龄
                if (int(age_) <= 17):
                    age_count[0] += age_info[index]  # 00后
                elif (int(age_) <= 22):  # 95后
                    age_count[1] += age_info[index]
                elif (int(age_) <= 27):  # 90后
                    age_count[2] += age_info[index]
                elif (int(age_) <= 37):  # 80后
                    age_count[3] += age_info[index]
                else:
                    age_count[4] += age_info[index]  # 80前
        age_labels = [u"00后", u"95后", u"90后", u"80后", u"80前"]

        for content in listen_songs_num_list:
            if (content < 100):
                listen_songs_num[0] += 1
            elif (content < 1000):
                listen_songs_num[1] += 1
            elif (content < 10000):
                listen_songs_num[2] += 1
            else:
                listen_songs_num[3] += 1
        for i in range(6):
            if (i == 0):
                title = u"%s:评论者<动态数目>分布" % song_or_singer_name
                labels = [u"0-10", u"10-50", u"50-100", u"100以上"]
                colors = ["red", "blue", "yellow", "green"]
                x = event_count
                plt.subplot(2, 3, i + 1)
                plt.pie(x, colors=colors, labels=labels, autopct="%1.1f%%")
                plt.title(title)
                # plt.legend(labels)
            elif (i == 1):
                title = u"%s:评论者<关注人数>分布" % song_or_singer_name
                labels = [u"0-10", u"10-30", u"30-50", u"50-100", u"100以上"]
                colors = ["red", "blue", "yellow", "green", "white"]
                x = follow_count
                plt.subplot(2, 3, i + 1)
                plt.pie(x, colors=colors, labels=labels, autopct="%1.1f%%")
                plt.title(title)
                # plt.legend(labels)
            elif (i == 2):
                title = u"%s:评论者<粉丝人数>分布" % song_or_singer_name
                labels = [u"0-10", u"10-100", u"100-1000", u"1000-10000", u"10000以上"]
                colors = ["red", "blue", "yellow", "green", "white"]
                x = fan_count
                plt.subplot(2, 3, i + 1)
                plt.pie(x, colors=colors, labels=labels, autopct="%1.1f%%")
                plt.title(title)
                # plt.legend(labels)
            elif (i == 3):
                title = u"%s:评论者<地区>分布" % song_or_singer_name
                colors = ["red", "blue", "yellow", "green", "white", "purple"]
                x = area_count
                plt.subplot(2, 3, i + 1)
                plt.pie(x, colors=colors, labels=area_labels, autopct="%1.1f%%")
                plt.title(title)
                # plt.legend(area_labels,loc='upper center', bbox_to_anchor=(0.1,0.9),ncol=1,fancybox=True,shadow=True)
            elif (i == 4):
                title = u"%s:评论者<年龄>分布" % song_or_singer_name
                colors = ["red", "blue", "yellow", "green", "white"]
                x = age_count
                plt.subplot(2, 3, i + 1)
                plt.pie(x, colors=colors, labels=age_labels, autopct="%1.1f%%")
                plt.title(title)
                # plt.legend(age_labels)
            else:
                title = u"%s:评论者<累计听歌>分布" % song_or_singer_name
                labels = [u"0-100", u"100-1000", u"1000-10000", u"10000以上"]
                colors = ["red", "blue", "yellow", "green"]
                x = listen_songs_num
                plt.subplot(2, 3, i + 1)
                plt.pie(x, colors=colors, labels=labels, autopct="%1.1f%%")
                plt.title(title)
                # plt.legend(labels)
        plt.tight_layout()
        plt.show()

    # sub_plot_months 测试
    def sub_plot_months_test(self):
        song_name = u"越长大越孤单"
        row = 3
        col = 4
        settings_dict = {
            "plot_type": "plot",
            "color": "g",
            "bar_width": 0.8,
            "fontsize": 10,
            "rotation": 50,
            "time_distance": "5D"
        }
        settings = []
        DateLists = ['2016-04', '2016-05', '2016-06', '2016-07', '2016-08', '2016-09', '2016-10', '2016-11', '2016-12',
                     '2017-01', '2017-02', '2017-03']
        for i in range(len(DateLists)):
            settings.append(settings_dict)
        self.sub_plot_months(song_name, DateLists, settings, row=row, col=col)

    # 绘制subplot 测试
    def subplot_test(self):
        song_names_list = [u"七里香", u"不要再孤单", u"All Too Well", u"刚好遇见你"]
        settings_dict = {"date_type": "%Y-%m-%d",
                         "plot_type": "bar",
                         "fontsize": 12,
                         "color": "r",
                         "bar_width": 0.4,
                         "rotation": 50,
                         "time_distance": "3D",
                         "min_date_Ymd": "2017-03-01",
                         "max_date_Ymd": "2017-12-31",
                         "min_date_Ym": "2013-01",
                         "max_date_Ym": "2017-12"
                         }
        settings = []
        for i in range(len(song_names_list)):
            settings.append(settings_dict)
        row = 2
        col = 2
        self.sub_plot_comments(song_names_list, settings, row=row, col=col)

    # plot_comments 函数测试
    def plot_comments_test(self):
        song_name = u"我从崖边跌落"
        settings = {
            "comment_type": False,
            "date_type": "%Y-%m-%d",
            "plot_type": "plot",
            "bar_width": 0.8,
            "rotation": 20,
            "color": "purple",
            "pie_colors": ["blue", "red", "coral", "green", "yellow"],
            "auto_pct": '%1.1f%%',
            "expl": [0, 0, 0.1, 0.3],  # 离开圆心的距离
            "time_distance": "3D",
            "min_date_Ymd": "2013-12-01",
            "max_date_Ymd": "2017-12-31",
            "min_date_Ym": "2013-01",
            "max_date_Ym": "2017-12"
        }
        self.plot_comments(song_name, settings)


if __name__ == '__main__':
    Processor = NetCloudProcessor()
    Processor.plot_comments_test()