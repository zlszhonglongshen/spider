#coding:utf-8
import urllib.request
import re
import os


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

        # ----------------------------------


# --------测试抓取酒店URL程序------------
# ----------------------------------
if __name__ == "__main__":
    count = 1
    getHotelUrl(count)