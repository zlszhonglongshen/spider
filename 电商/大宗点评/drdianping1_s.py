'''
程序名：   drdianping1_s
功能：    根据已有的的"大众点评网"酒店主页的URL地址，自动抓取所有用户的"ID、name、评分、时间保存下来"。
语言：    python3.4
创建时间： 2016-4-10
作者:     dairen
'''
import urllib.request
import re
import time
import random

SleepNum = 0     # 抓取页面的间隔时间，可为0

# 获取指定time中的年份
def get_year(time):
    year = time.split('-')[0]
    return int(year)

def no_previous00(timelist):
    for t in range(0,len(timelist)):
        year = get_year(timelist[t])
        if year<0:
            return False
        else:
            continue
    return True

# 统计所有酒店的评价信息，存入文本
def getRatingAll(fileIn, fileOut="D:/rating.txt"):
    count =1          # 计数，显示进度
    breaknumber = 0   # 计数，发生异常的url数
    fileOp = open(fileOut, 'a', encoding="utf-8")
    fileOp.write( "hotelid \t\t userid \t\t username \t\t rate_room  \t\t rate_service \t\t rate_total \t\t rate_time \n")
    fileOp.close()
    for line in open(fileIn,'r'):     # 逐行读取并处理文件，即hotel的url
        try:
            # 酒店编号
            hotelid = line.strip('\n').split('/')[4]
            print('该酒店的hotelid是 : ', hotelid)

            # 拼凑出该酒店第一页"评论页面"的url
            url = line.strip('\n') + "/review_more"
            print('该酒店第一页"评论页面"的url是', url)

            # 模拟浏览器,打开url
            headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko')
            opener = urllib.request.build_opener()
            opener.addheaders = [headers]
            data = opener.open(url).read()

            save_path = 'D:\\temp.out'
            f_obj = open(save_path, 'wb')
            f_obj.write(data)
            f_obj.close()
            data = data.decode('utf-8', 'ignore')

            # 对于下面这段str匹配
            #    title="">全部点评</a><em class="col-exp">(1195)</em></span>
            rate_number = re.compile(r'全部点评</a><em class="col-exp">\((.*?)\)</em></span>', re.DOTALL).findall(data)
            if rate_number == '':
                continue
            # 列表形式,这里不是俩括号的意思，而是用转义符把1195外面的圆括号分开，flag为DOTALL可以匹配任何字符包括换行（newline）
            rate_number = int(''.join(rate_number))  # 把列表转换为str，把可迭代列表里面的内容用‘ ’连接起来成为str，再进行类型转换
            print("测试：第%d家酒店的评论数为%d" % (count, rate_number))
            count += 1

            if rate_number == 0:  # 如果评论数为0，跳过，处理下一个酒店URL
                # count = count+1
                print("----------")
                continue
            else:
                # 解析评分
                pages = int(rate_number / 20) + 1  # 由评论数计算页面数,点评网每页最多20条评论.
                # print(pages)

                for i in range(1, pages + 1):
                    # 打开页面
                    add_url = url + '?pageno=' + str(i)
                    headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko')
                    opener = urllib.request.build_opener()
                    opener.addheaders = [headers]
                    data = opener.open(add_url).read()
                    data = data.decode('utf-8', 'ignore')

                    #    <a target="_blank" rel="nofollow" href="/member/8450012" user-id="8450012" class="J_card">
                    #      <img title="灵燕儿" alt="灵燕儿" src="http://i2.dpfile.com/pc/0ffc32ea67e4e872fc50ec7c04effcec(48c48)/thumb.jpg">

                    # 获取用户ID列表
                    userid = re.compile(r'user-id="(.*?)" class="J_card">', re.DOTALL).findall(
                        data)  # 每个list有20条id，全print出来
                    print('userid', userid)
                    # 获取用户的名字
                    username = re.compile(r'<img title="(.*?)" alt=', re.DOTALL).findall(data)
                    print('username', username)

                    # 评价时间
                    #   <span class="time">04-04&nbsp;&nbsp;更新于16-04-04 20:45</span>
                    rate_time = re.compile(r'<span class="time">(..-..)', re.DOTALL).findall(data)
                    print("评价时间:", rate_time)

                    # 单项评分
                    rate_room = re.compile(r'<span class="rst">房间(.*?)<em class="col-exp">', re.DOTALL).findall(data)
                    rate_envir = re.compile(r'<span class="rst">环境(.*?)<em class="col-exp">', re.DOTALL).findall(data)
                    rate_service = re.compile(r'<span class="rst">服务(.*?)<em class="col-exp">', re.DOTALL).findall(data)
                    print("房间评分:\n", rate_room)
                    print("环境评分:\n", rate_envir)
                    print("服务评分:\n", rate_service)

                    # 总评分
                    #   <span title="很好" class="item-rank-rst irr-star40"></span>
                    rate_total = re.compile(r'" class="item-rank-rst irr-star(.*?)0"></span>', re.DOTALL).findall(data)
                    print("总评分", rate_total)
                    mink = min(int(len(userid)), int(len(rate_total)), int(len(rate_room)))
                    print('mink:  ', mink)

                    # if no_previous10(rate_time):   # 只抓取2010年之后的评论

                    # 写入文件； 首先判断，如果每项数目都对应，则认为各项列表正确（一般是20）

                    # if len(userid)==len(rate_total)==len(rate_room)==len(rate_envir)==len(rate_service)==len(rate_time): #一般每页是20项评论
                    fileOp = open(fileOut, 'a', encoding="utf-8")
                    for k in range(0, mink):
                        fileOp.write('%s \t\t %s \t\t %s \t\t %s \t\t %s \t\t %s \t\t %s \t\t\n' % (hotelid, userid[k], username[k], rate_room[k], rate_service[k], rate_total[k], rate_time[k]))
                    fileOp.close()
            # 酒店数目+1,
            count = count+1
            time.sleep(SleepNum)
        # 异常处理：若异常，存储该url到新文本中，继续下一行的抓取
        except:
            file_except = open('D:/exception.txt','a')
            file_except.write(line)
            breaknumber = breaknumber+1
            if breaknumber == 20:              #异常url的数目累积到20时，终止程序。
                print('count:   ',count)
                break
            else:
                continue


#----------------------------------
#------------测试爬虫程序------------
#----------------------------------
if __name__ == "__main__":
    fileIn = ".\hotel.txt"
    getRatingAll(fileIn)

















