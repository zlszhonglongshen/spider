import urllib
import json
import re


class JdPrice(object):
    """
    对获取京东商品价格进行简单封装
    """

    def __init__(self, url):
        self.url = url
        self._response = urllib.urlopen(self.url)
        self.html = self._response.read()

    def get_product(self):
        """
        获取html中，商品的描述(未对数据进行详细处理，粗略的返回str类型)
        """
        product_re = re.compile(r'compatible: true,(.*?)};', re.S)
        product_info = re.findall(product_re, self.html)[0]
        return product_info

    def get_product_skuid(self):
        """
        通过获取的商品信息，获取商品的skuid
        """
        product_info = self.get_product()
        skuid_re = re.compile(r'skuid: (.*?),')
        skuid = re.findall(skuid_re, product_info)[0]
        return skuid

    def get_product_name(self):
        """
        通过获取的商品信息，获取商品的name
        """
        # '\u4e2d\u6587'.decode('unicode-escape') （你可能需要print它才能看到结果）
        product_info = self.get_product()
        # 源码中名称左右有两个',所以过滤的时候应该去掉
        name_re = re.compile(r"name: '(.*?)',")
        name = re.findall(name_re, product_info)[0]
        return name.decode('unicode-escape')  # 将其转换为中文

    def get_product_price(self):
        """
        根据商品的skuid信息，请求获得商品price
        :return:
        """
        price = None

        # 得到产品的序号和名称，取价格的时候会用得到
        skuid = self.get_product_skuid()
        name = self.get_product_name()
        print name

        # 通过httpfox检测得知，每次网页都会访问这个网页去提取价格嵌入到html中
        url = 'http://p.3.cn/prices/mgets?skuIds=J_' + skuid + '&type=1'

        # json调整格式，并将其转化为utf-8，列表中只有一个字典元素所以取出第一个元素就转化为字典
        price_json = json.load(urllib.urlopen(url))[0]

        # p对应的价格是我们想要的
        if price_json['p']:
            price = price_json['p']
        return price


if __name__ == '__main__':
    print "+" * 20 + "welcome to 京东放养的爬虫" + "+" * 20
    url = 'http://item.jd.com/3133927.html'
    jp = JdPrice(url)
    print jp.get_product_price()
    print "+" * 20 + "welcome to 京东放养的爬虫" + "+" * 20





# -*- coding:utf-8 -*-

import urllib2
import json
import re

SearchIphoneUrl = 'http://search.jd.com/Search?keyword=%E8%8B%B9%E6%9E%9C%E6%89%8B%E6%9C%BA&enc=utf-8&qr=&qrst=UNEXPAND&as_key=title_key%2C%2C%E6%89%8B%E6%9C%BA&rt=1&stop=1&click=&psort=1&page=1'
header = {
    'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36 SE 2.X MetaSr 1.0',
    'Accept': '*/*'}


def getHtmlSrc(url, header):
    req = urllib2.Request(url, header)
    res = urllib2.urlopen(url, timeout=5)
    htmlSrc = res.read()
    return htmlSrc


def saveHtmlSrc(url):
    html = getHtmlSrc(url, header)
    with open('jd_iphone.txt', 'w') as f:
        f.write(html)


saveHtmlSrc(SearchIphoneUrl)
print '++++++++++++++++++++京东放养的爬虫++++++++++++++++++++'

with open('jd_iphone.txt', 'r') as fhtml:
    localhtml = fhtml.read()  # .replace("'",'"').replace(' ','')
    # print(localhtml)
    for skuid in re.findall('<li sku="\d+">', localhtml):
        # 商品编号
        sku = skuid.split('"')[1]
        # 手机名称
        pname = re.search('''''<font class="skcolor_ljg">苹果</font>(.*?)<font class="skcolor_ljg">''',
                          localhtml)  # 正则取商品名称html
        # 手机价格
        price = re.search('''''<strong class="J_%s" data-price="(.*?)">''' % sku, localhtml)
        if (pname != '' and price != ''):
            print "商品编号：%s" % sku
            print "名称：%s\n价格：%s\n\n" % (pname.group(1), price.group(1))

print '++++++++++++++++++++京东放养的爬虫++++++++++++++++++++'

