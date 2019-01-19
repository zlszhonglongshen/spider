#coding:utf-8
__author__='Johnson'

import pandas as pd
import urllib.request
import urllib.error
import re
import time
import socket

class Spider():
    #初始化
    def __init__(self,url):
        self.url = url
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  # 设置代理
        self.headers = {'User-Agent': self.user_agent}  # 设置头信息
        self.outputPath = 'spiderResult.csv'  # 输出路径

    #读取链接内容
    def readURL(self):
        try:
            request = urllib.request.Request(self.url, headers=self.headers)  # 请求链接
            response = urllib.request.urlopen(request, timeout=20)  # 打开链接，超过20秒则抛出异常
            content = response.read()
            content = content.decode('gbk')  # 读取链接内容并解码
            print('读取链接成功！')
            return content
        except socket.error as e1:  # 读取链接异常，抛出
            print(e1)
        except urllib.error.URLError as e2:
            print(e2)
    #根据正则表达式爬取链接内容
    def spiderByPattern(self,pattern,content):
        data = re.findall(pattern, content)  # 根据正则表达式获取数据
        data = pd.DataFrame(data)  # 转化格式
        return data

#处理数据
def formatData(data):
    for i in range(len(data)):
        data[i] = str(data[i]).replace('\n','') #去掉换行符
    return data


def DealTest():
    #获取当当网的商品编码
    f = open('ddjson.txt') #查看网页元素得到的商品分类文件
    data = f.read()
    f.close()
    pattern = re.compile('category#dd#cid(.*?).html.*?"n":"(.*?)"',re.S) # 商品ID的正则匹配
    cids = re.findall(pattern,data) #商品ID
    d = {}
    for item in cids:
        d[item[0]] = item[1].encode().decode('unicode_escape')
    cid = list(d.keys()) #商品ID
    #跳过爬取错误
    try:
        # 读取之前爬取过的文件，第一次爬取不需要读取
        a = pd.read_csv('spiderResult.csv', header=None, sep='|', encoding='gbk',
                        error_bad_lines=False).ix[:, 4]
        readedCid = set(a)  # 已经爬取过的商品编码
    except:
        readedCid = []
    for tmpCid in cid:
        if tmpCid in readedCid: continue  # 当前爬取的商品编码是否已经爬取过
        tmpPage = 1  # 当前页号
        url = 'http://category.dangdang.com/pg' + str(tmpPage) + '-cid' + tmpCid + '.html'  # 链接
        spider = Spider(url)  # 创建爬虫类
        content = spider.readURL()  # 读取链接内容

        pattern = re.compile('<ul.*?class="paging".*?<li.*?class="page_input".*?共(.*?)页', re.S)  # 获取总页数
        try:
            pageCount = int(re.findall(pattern, content)[0])
        except:
            print(url, '找不到页数')
            continue
        for tmpPage in range(1, pageCount + 1):
            url = 'http://category.dangdang.com/pg' + str(tmpPage) + '-cid' + tmpCid + '.html'  # 链接
            print('正爬取链接：', url, '\t第', tmpPage, '页，共', pageCount, '页\t', d[tmpCid], time.asctime(time.localtime()))
            spider = Spider(url)  # 创建爬虫类
            content = spider.readURL()  # 读取链接内容
            try:
                pattern = re.compile(
                    '<li.*?class="line.*?".*?<p.*?class="price".*?<span.*?class="price_n">&yen;(.*?)</span'  # 商品价格
                    '.*?<p.*?class="name".*?target="_blank".*?>(.*?)</a>'  # 商品名称
                    '.*?<p.*?class="subtitle".*?>(.*?)</p>'  # 副标题
                    '.*?<p.*?class="star".*?style="display.*?".*?target="_blank".*?>(.*?)</a>'  # 商品评论数
                    , re.S)
                data = spider.spiderByPattern(pattern, content)  # 根据正则表达式获取数据
                data.ix[:, 4] = tmpCid
                data.ix[:, 5] = d[tmpCid]
                spider.writeURL(data)  # 写入数据
            except:
                try:
                    pattern = re.compile(
                        '<li.*?name="lb".*?<p.*?class="price".*?<span.*?class="price_n">&yen;(.*?)</span'  # 商品价格
                        '.*?<p.*?class="name".*?target="_blank".*?>(.*?)</a>'  # 商品名称
                        '.*?<p.*?class="subtitle".*?>(.*?)</p>'  # 副标题
                        '.*?<p.*?class="star".*?style="display.*?".*?target="_blank".*?>(.*?)</a>'  # 商品评论数
                        , re.S)
                    data = spider.spiderByPattern(pattern, content)  # 根据正则表达式获取数据
                    data.ix[:, 4] = tmpCid
                    data.ix[:, 5] = d[tmpCid]
                    spider.writeURL(data)  # 写入数据
                except:
                    print('爬取链接出错!')

if __name__ == '__main__':
    DealTest()




