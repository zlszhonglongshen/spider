#coding:utf-8
import urllib.request
import re


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


# ----------------------------------
# --------------测试程序---------------
# ----------------------------------
if __name__ == "__main__":
    url = "http://www.dianping.com/shop/4067980"

    HotelName = u"龙猫主题公寓"
    # FileOut ='G:/EclipseWorkspace/Python/src/InternetWorm/Image/'+HotelName
    FileOut = '.\\image\\' + HotelName
    getPicture(url, FileOut)