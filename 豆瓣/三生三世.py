# encoding:UTF-8
import urllib2
from bs4 import BeautifulSoup
import requests
import re
import random
import sys
import time


def get_ip_list():
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list


def get_random_ip():
    ip_list = get_ip_list()
    proxy_list = []
    for ip in ip_list:
        proxy_list.append(ip)
    proxy_ip = random.choice(proxy_list)
    return proxy_ip


class MovieComment:
    def __init__(self):
        # 设置默认编码格式为utf-8
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.start = 0  # 爬虫起始位置
        self.param = '&limit=20&sort=new_score&status=P'
        # User-Agent是用户代理，用于使服务器识别用户所使用的操作系统及版本、浏览器类型等，可以认为是爬虫程序的伪装。
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3343.4 Safari/537.36',
            'cookie': 'll="118281"; bid=H1tJ8IH3Gp8; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1519717546%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DgOXPCxE4HSq9GOGH0QGNS9dAkHhJbP12wWRGUmpv8zCDYcX5_VJ8_p9Cf-L0ill0%26wd%3D%26eqid%3De599da8300002976000000065a950c9c%22%5D; _pk_ses.100001.8cb4=*; ps=y; ue="593956670@qq.com"; __yadk_uid=FrGL1AzxzAW9MuiaPwUabltQbMoPAp9F; push_noty_num=0; push_doumail_num=0; __utma=30149280.1063662806.1519717562.1519717562.1519717562.1; __utmz=30149280.1519717562.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login; __utmt=1; __utmv=30149280.321; _pk_id.100001.8cb4=15a8a6f6246a0809.1519717546.1.1519717590.1519717546.; __utmc=30149280; __utmb=30149280.6.9.1519717591421'}
        self.commentList = []
        self.filePath = 'h:/eebc.txt'
        self.proxies = get_random_ip()  # 定义代理IP

    def getPage(self):
        try:
            URL = 'https://movie.douban.com/subject/26430107/comments?start=' + str(self.start)
            proxy = urllib2.ProxyHandler({"http": self.proxies})
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
            request = urllib2.Request(url=URL, headers=self.headers)
            response = urllib2.urlopen(request, timeout=5)
            page = response.read().decode('utf-8')
            pageNum = (self.start + 20) / 20
            print '正在抓取第' + str(pageNum) + '页数据...'
            self.start += 20
            if self.start % 100 == 0:
                self.proxies = get_random_ip()
            return page
        except (urllib2.URLError, Exception), e:
            if hasattr(e, 'reason'):
                print '抓取失败，具体原因：', e.reason
                # 超时响应
                response = urllib2.urlopen(request, timeout=5)
                page = response.read().decode('utf-8')
                pageNum = (self.start + 20) / 20
                print '正在抓取第' + str(pageNum) + '页数据...'
                self.start += 20
                if self.start % 400 == 0:  # 设置获取IP间隔页数
                    self.proxies = get_random_ip()
                return page

    def getMovie(self):
        pattern = re.compile(u'<div.*?class="avatar">.*?'
                             + u'<a.*?title="(.*?)".*?href=".*?">.*?</a>.*?'
                             + u'<p.*?class="">(.*?)</p>', re.S)  # 正则表达式
        while self.start <= 20000:  # 爬虫结束位置
            page = self.getPage()
            time.sleep(5)
            comments = re.findall(pattern, page)
            for comment in comments:
                self.commentList.append([comment[0], comment[1].strip()])  # 将捕获组数据写入评论List中

    def writeTxt(self):
        fileComment = open(self.filePath, 'w')
        try:
            for comment in self.commentList:
                fileComment.write(comment[1] + '\r\n\r\n')
            print '文件写入成功...'
        finally:
            fileComment.close()

    def main(self):
        print '正在从《二十二》电影短评中抓取数据...'
        self.getMovie()
        self.writeTxt()
        print '抓取完毕...'


DouBanSpider = MovieComment()
DouBanSpider.main()

