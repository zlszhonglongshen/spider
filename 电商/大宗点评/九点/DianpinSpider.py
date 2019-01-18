#coding:utf-8
import urllib.request
import re
import time
# import picture  # 获取酒店图片
# import urlspider  # 获取酒店的URL
# import position
import os
import random
# import PriceAndScores


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
    print(scores)
    # 获取酒店价格
    # price = re.compile(r'<span class="price">(.*?)</span>', re.DOTALL).findall(data)
    # price = int(''.join(price))
    # print(price )
    return  scores


def to_base36(value):
    """将10进制整数转换为36进制字符串
    """
    if not isinstance(value, int):
        raise (TypeError("expected int, got %s: %r" % (value.__class__.__name__, value)))

    if value == 0:
        return "0"

    if value < 0:
        sign = "-"
        value = -value
    else:
        sign = ""

    result = []

    while value:
        (value, mod) = divmod(value, 36)
        result.append("0123456789abcdefghijklmnopqrstuvwxyz"[mod])

    return (sign + "".join(reversed(result)))


def getPosition(C):
    """解析大众点评POI参数
    """
    digi = 16
    add = 10
    plus = 7
    cha = 36
    I = -1
    H = 0
    B = ''
    J = len(C)
    G = ord(C[-1])
    C = C[:-1]
    J -= 1

    for E in range(J):
        D = int(C[E], cha) - add
        if D >= add:
            D = D - plus
        B += to_base36(D)
        if D > H:
            I = E
            H = D

    A = int(B[:I], digi)
    F = int(B[I + 1:], digi)
    L = (A + F - int(G)) / 2
    latitude = float(F - L) / 100000
    longitude = float(L) / 100000
    return longitude, latitude

def getHotelUrl(count):
    filename = 'HotelUrl.txt'
    if os.path.exists(filename):
        #         print("Yes")
        os.remove(filename)
    print("正在获取广州市天河区附近热门酒店的URL，保存至HotelUrl.txt")
    for k1 in range(1, 51):
        tempurlpag = "http://www.dianping.com/guangzhou/hotel/r22c354p" + str(k1) + "o10"
        # 下面对于当前页拿到每个酒店网址并加入队列
        headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko')
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        op = opener.open(tempurlpag)
        data = op.read().decode(encoding='UTF-8')
        linkre = re.compile(r'data-shop-url="(.*?)"\r\n        data-hippo', re.DOTALL).findall(data)
        #         print(linkre)

        for k2 in range(0, len(linkre)):
            tempurlhotel = "http://www.dianping.com/shop/" + linkre[k2]
            fileOp = open(filename, 'a', encoding="utf-8")
            fileOp.write(str(count) + "\t" + tempurlhotel + '\n')
            fileOp.close()
            count += 1
            # print('目前是第:  %d  页的第： %d  个酒店，其地址是 ：%s'%(k1+1,k2+1,tempurlhotel))
        print('第:  %d  页抓取完成！' % k1)

def getPicture(url, FileOut):
    webPage = urllib.request.urlopen(url)
    data = webPage.read()
    data = data.decode('UTF-8')

    picture_temp = re.compile(r'<img src="(.*?)%', re.DOTALL).findall(data)
    picture_url = picture_temp[0:5]  # 只需要获取前五张图片即可
    # print(picture_url)
    for i in range(0, 5):
        web = urllib.request.urlopen(picture_url[i])
        # print(web)
        itdata = web.read()
        # print(itdata)
        f = open(FileOut + str(i + 1) + '.jpg', "wb")
        f.write(itdata)
        f.close()
# 统计所有酒店的评价信息，存入文本
def getRatingAll(fileIn):
    count = 0  # 计数，显示进度
    websitenumber = 0
    for line in open(fileIn, 'r'):  # 逐行读取并处理文件，即hotel的url
        count = line.split('\t')[0]
        line = line.split('\t')[1]
        websitenumber += 1
        print("正在抓取第%s个网址的酒店信息" % (websitenumber))
        try:
            print("正在抓取第%s家酒店的信息，网址为%s" % (count, line.strip('\n')))
            # 获取酒店编号
            hotelid = line.strip('\n').split('/')[4]
            # print('该酒店的hotelid是 : ', hotelid)

            # 拼凑出该酒店第一页"评论页面"的url
            url = line.strip('\n') + "/review_more"
            # print('该酒店第一页"评论页面"的url是', url)

            # 模拟浏览器,打开url
            headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko')
            opener = urllib.request.build_opener()
            opener.addheaders = [headers]
            data = opener.open(url).read()
            # print(data)  当访问大众点评网过于次数频繁的时候，大众点评网的反爬虫技术会封锁本机的IP地址，此时data就会出现异常，无法打印正常的html
            data = data.decode('utf-8', 'ignore')
            # print(data)

            # 获取酒店用户评论数目
            rate_number = re.compile(r'<span>网友点评</span> <span class="count">\((.*?)\)</span></a>', re.DOTALL).findall(data)
            rate_number = int(''.join(rate_number))  # 把列表转换为str，把可迭代列表里面的内容用‘ ’连接起来成为str，再进行类型转换
            print("第%d家酒店的评论数为%s" % (websitenumber, rate_number))

            if (rate_number < 100):  # 若酒店评论数目少于100条，则不跳过该酒店，不再挖取信息
                continue

            # 获取酒店名称和地址
            opener1 = urllib.request.build_opener()
            opener1.addheaders = [headers]
            hotel_url = opener1.open(line).read()
            hotel_data = hotel_url.decode('utf-8')  # ignore是忽略其中有异常的编码，仅显示有效的编码
            # print(hotel_data)  #当访问大众点评网过于次数频繁的时候，大众点评网的反爬虫技术会封锁本机的IP地址，此时hotel_data就会出现异常，无法打印正常的html
            # 获取酒店名称
            shop_name = re.compile(u'<h1 itemprop="name">(.*?)</h1>', re.DOTALL).findall(hotel_data)
            shop_name = str(''.join(shop_name))  # 类型转换
            shop_name = shop_name.strip()  # 去掉字符串中的换行符
            # 获取酒店地址
            address = re.compile(u'<span class="name">地址：</span> <span class="value">(.*?)</span>', re.DOTALL).findall(
                hotel_data)
            address = str(''.join(address))
            # print(address)

            # 获取酒店经纬度
            # poi = re.compile(r'poi: \"(.*?)\",', re.DOTALL).findall(hotel_data)
            # poi = str(''.join(poi))
            # (longitude, latitude) = getPosition(poi)
            # print("longitude:%s°E,latitude:%s°N" % (longitude, latitude))

            # 获取酒店评分和酒店价格
            (scores) = getPriceAndScores(line.strip('\n'))

            # 获取酒店图片
            # PictureOut = '.\\image\\' + str(count) + " " + shop_name
            # getPicture(line.strip('\n'), PictureOut)

            # 保存酒店信息
            fileOut = '.\\hotel\\' + str(count) + " " + shop_name + '.txt'
            if os.path.exists(fileOut):
                os.remove(fileOut)
            fileOp = open(fileOut, 'a', encoding="utf-8")
            fileOp.write("酒店名称: %s\n酒店网址： %s\n酒店评分： %d stars\n评论数量: %s\n" % (
            shop_name, address,  scores, rate_number))
            fileOp.write("酒店ID \t\t 用户ID \t\t 用户名字 \t\t 房间评分  \t\t 服务评分 \t\t 用户总评分 \t\t 评价时间 \n")
            fileOp.close()

            FileName = '.\\hotel\\' + str(count) + " " + shop_name + ' 用户评论.txt'
            if os.path.exists(FileName):
                os.remove(FileName)
                # 解析评分
            pages = int(rate_number / 20) + 1  # 由评论数计算页面数,大众点评网每页最多20条评论.
            # print(pages)
            for i in range(1, pages + 1):
                # 打开页面
                add_url = url + '?pageno=' + str(i)
                headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko')
                opener = urllib.request.build_opener()
                opener.addheaders = [headers]
                data = opener.open(add_url).read()
                data = data.decode('utf-8', 'ignore')

                # 获取酒店评论用户ID列表
                userid_temp = re.compile(
                    r'<a target="_blank" rel="nofollow" href="/member/(.*?)" user-id="(.*?)" class="J_card">',
                    re.DOTALL).findall(data)
                userid = [None] * len(userid_temp)
                for i in range(0, len(userid_temp)):
                    userid[i] = userid_temp[i][0]

                # 获取酒店评论用户的名字
                username = re.compile(r'<img title="(.*?)" alt=', re.DOTALL).findall(data)

                # 获取评价时间
                rate_time = re.compile(r'<span class="time">(..-..)', re.DOTALL).findall(data)

                # 获取单项评分
                rate_room = re.compile(r'<span class="rst">房间(.*?)<em class="col-exp">', re.DOTALL).findall(data)
                #                 rate_envir = re.compile(r'<span class="rst">位置(.*?)<em class="col-exp">', re.DOTALL).findall(data)
                rate_service = re.compile(r'<span class="rst">服务(.*?)<em class="col-exp">', re.DOTALL).findall(data)

                # 获取总评分
                rate_total = re.compile(r'" class="item-rank-rst irr-star(.*?)0"></span>', re.DOTALL).findall(data)
                mink = min(int(len(userid)), int(len(rate_total)), int(len(rate_room)))

                # 获取用户评论
                user_comments = re.compile(r'<div class="J_brief-cont">(.*?)</div>', re.DOTALL).findall(data)
                user_comments = str(''.join(user_comments))  # 类型转换
                user_comments = user_comments.strip()  # 去掉字符串中的换行符
                # print(user_comments)

                # 将除酒店评论外的信息写入文件
                fileOp = open(fileOut, 'a', encoding="utf-8")
                for k in range(0, mink):
                    fileOp.write('%s \t\t %s \t\t %s \t\t %s \t\t %s \t\t %s \t\t %s \t\t\n' % (
                    hotelid, userid[k], username[k], rate_room[k], rate_service[k], rate_total[k], rate_time[k]))
                fileOp.close()

                # 将酒店评论写入另外的文件
                CommentsFile = open(FileName, 'a', encoding="utf-8")
                CommentsFile.write(user_comments.strip('\n'))
                CommentsFile.close()
                sleepNum = random.randint(0, 2)
                time.sleep(sleepNum)  # 当访问过频的时候，大众点评网的发爬虫技术可能会临时封锁我们的ip，所以可以通过设定时间来调整爬取速度，建议慢速爬取。或者通过代理ip来避免反爬虫技术封锁IP
                print(sleepNum)
            print("成功挖取第%s酒店的信息\n" % (count))

        # 异常处理：若异常，存储该url到新文本中，继续下一行的抓取
        except:
            print("第%s个酒店网址的信息抓取失败\n" % (websitenumber))  # 发生异常，无法成功爬取有用信息，抓取失败
            exceptionFile = 'exception.txt'
            file_except = open(exceptionFile, 'a')
            file_except.write("%s\t\t%s" % (str(websitenumber), line))  # 将爬取酒店信息时发生异常的网址保存起来


#主函数爬虫代码
if __name__ == "__main__":
    getHotelUrl(1)
    fileIn = "HotelUrl.txt"  # 需要爬取酒店的网址
    getRatingAll(fileIn)  # 抓取酒店评论页面的间隔时间，单位为秒，可为0
