#coding:utf-8
import urllib.request
import re


## 获取酒店名称和地址
def getPriceAndScores(url):
    # url = url.replace('www.', 'm.')
    # print(url)
    opener = urllib.request.build_opener()
    headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko')
    opener.addheaders = [headers]
    data = opener.open(url).read()
    data = data.decode('utf-8')  # ignore是忽略其中有异常的编码，仅显示有效的编码

    # 获取酒店总评分
    scores = re.compile(r'<span class="score">(.*?)</span>', re.DOTALL).findall(data)
    scores=str(' '.join(scores))
    # scores = int(scores[0]) / 10
    # print(scores)
    # 获取酒店价格
    price = re.compile(
                    r'<a target="_blank" rel="nofollow" href="/member/(.*?)" user-id="(.*?)" class="J_card">',
                    re.DOTALL).findall(data)
    # price = int(''.join(price))
    # print(price )
    return price, scores


if __name__ == "__main__":
    url = "http://www.dianping.com/shop/2256811"
    (price, scores) = getPriceAndScores(url)
    print(price)
    print(scores)