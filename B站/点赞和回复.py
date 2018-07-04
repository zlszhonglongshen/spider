# -*- coding:utf-8 -*-
# 查询点赞和回复提醒：http://message.bilibili.com/api/notify/query.notify.count.do
# 查询标签："tag_name":"灵异", http://api.bilibili.com/x/tag/archive/tags?aid=
# 查询UP主相关：http://api.bilibili.com/cardrich?mid=
# 查询UP主的作品相关：http://api.bilibili.com/vipinfo/default?mid=

# import urllib
# import urllib2
# import chardet

import requests
import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# requests工具箱请求服务器
def getHTMLText(url, agent):
    try:
        headers = {'User-Agent': agent}
        r = requests.get(url, timeout=30, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '获取网页信息失败'


# Headers查询头
agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36' \
       ' (KHTML, like Gecko) Chrome/50.0.2661.102 ' \
       'Safari/537.36 '
Query_Amount = 100                # 待查询的视频个数，设为100查前100个


f = open('test.txt', 'w')         # 打开待写入的txt文件
# sys.stdout = f                    # 将缓冲区写入，如果需要输出到test.txt中取消注释

for numAv in range(1, Query_Amount + 1):

    # 视频相关目标url
    try:
        url = 'http://www.bilibili.com/video/av' + str(numAv)
        resp = getHTMLText(url, agent)
        url2 = 'http://api.bilibili.com/archive_stat/stat?aid=' + str(numAv)
        resp2 = getHTMLText(url2, agent)
        url3 = 'http://api.bilibili.com/x/tag/archive/tags?aid=' + str(numAv)
        resp3 = getHTMLText(url3, agent)
    except:
        print '查询Bilibili服务器失败'
        continue

    if re.search('<div class="error-panel article-error"', resp):
        print '\n\n\n视频av' + str(numAv) + '已经删除\n'
        continue

    # 视频相关正则表达式
    reg_Title = r'<h1 title="(.*?)">.*?</h1>'
    reg_Author = r'card="(.*?)" mid=".*?" title=".*?"'
    reg_Space = r'<a href="//space.bilibili.com/.*?" card=".*?" mid="(.*?)" title=".*?"'
    reg_Clicks = r'"view":(.*?),'
    reg_Comments = r'"reply":(.*?),'
    reg_Tags = r'"tag_name":"(.*?)",'
    reg_Content = r'"content":"(.*?)"'
    reg_Time = r'<time itemprop="startDate" datetime=".*?"><i>(.*?)</i></time>'

    # UP主相关目标url
    up_ID = "".join(re.findall(reg_Space, resp))
    url4 = 'http://api.bilibili.com/cardrich?mid=' + up_ID
    resp4 = getHTMLText(url4, agent)
    url5 = 'http://api.bilibili.com/vipinfo/default?mid=' + up_ID
    resp5 = getHTMLText(url5, agent)

    # UP主相关相关正则表达式
    reg_Fans = r'"fans":(.*?),'
    reg_Works = r'"archiveCount":(.*?)}'
    reg_Mortal = r'"sign":"(.*?)",'
    reg_Birthday = r'"birthday":"(.*?)",'
    reg_Gender = r'"sex":"(.*?)",'

    # 查询
    title = "".join(re.findall(reg_Title, resp))
    time = "".join(re.findall(reg_Time, resp))
    space = 'http://space.bilibili.com/' + up_ID
    author = "".join(re.findall(reg_Author, resp))
    works = "".join(re.findall(reg_Works, resp5))
    clicks = "".join(re.findall(reg_Clicks, resp2))
    comments = "".join(re.findall(reg_Comments, resp2))
    fans = "".join(re.findall(reg_Fans, resp4))
    tags = re.findall(reg_Tags, resp3)
    content = "".join(re.findall(reg_Content, resp3))
    mortal = "".join(re.findall(reg_Mortal, resp4)).decode('unicode_escape')
    birthday = "".join(re.findall(reg_Birthday, resp4))
    gender = "".join(re.findall(reg_Gender, resp4)).decode('unicode_escape')

    # 内容为空时改为未填
    if content == '':
        content = '未填'

    # 箴言为空时改为未填
    if mortal == '':
        mortal = '未填'

    # tag处理整合成字符串
    if len(tags) == 0:
        tags = '未填'
    else:
        temp = '[' + tags[0] + ']'
        if len(tags) > 1:
            for j in range(1, len(tags)):
                temp = temp + '; [' + tags[j] + ']'
            tags = temp
    tags = "".join(tags)

    # 调试用输出
    # print resp
    # print resp2
    # print resp3
    # print
    # print '正在查询：' + str(numAv) + '/' + str(Query_Amount)

    print '\n\n'
    print '\n\n' + '='*100
    print '视频编号：av' + str(numAv)
    print '视频标题：', title
    print '视频标签：', tags
    print '视频内容：', content
    print '视频点击量：', clicks
    print '视频评论数：', comments
    print '投稿时间：', time
    print '视频地址：', url
    print
    print '作者up主名：', author
    print 'up主ID：', up_ID
    print 'up主空间地址：', space
    print 'up主粉丝数：', fans
    print 'up主作品数：', works
    print 'up主性别：', gender
    print 'up主生日：', birthday
    print 'up主箴言：', mortal
f.close()