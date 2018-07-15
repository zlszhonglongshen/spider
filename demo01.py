#coding:utf-8
from bs4 import BeautifulSoup
import requests
import time
import pymysql
import xlwt
from datetime import datetime

"""
data = {'html': 'http://bj.xiaozhu.com/fangzi/2803985763.html',
        'title': '国贸双井10号线苹果酒店式公寓',
        'address': '北京市朝阳区苹果社区北区',
        'price': '428',
        'pic': 'http://image.xiaozhustatic1.com/00800533/60253184180012004b993d38.jpg',
        'host_name': '阳光艳艳',
        'host_gender': '女'
        }
"""
def excel(i,data):
    #向txt中文件里写数据
    with open("Data.txt",'a+') as f:
        f.write(str(i) + "、" + " [名称]:" + data['title'] + "[姓名]：" + data['host_name'] + " [性别]:" + data[
            'host_gender'] + " [地址]:" + data['address'] + " [价格]:" + data['price'] + " [图片地址]:" + data[
                    'pic'] + " [网址]:" + data['html'] + "\n\n")


def Mysqlconnt(data):
    """数据库操作"""
    db = pymysql.connect(host="localhost",
                       port=3306,
                       user="root",
                       passwd="",
                       db="mysql",
                       charset="utf8")#添加编码格式设置
    cursor = db.cursor()
    sql = "insert into xiaozhu(host_name,host_gender,title,address,price,pic,html) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',%s,\'%s\',\'%s\')" % (data['host_name'],data['host_gender'],data['title'],data['address'],data['price'],data['pic'],data['html'])
    sql2 = "CREATE TABLE IF NOT EXISTS xiaozhu(host_name VARCHAR(40),host_gender VARCHAR(40),title,address VARCHAR(40),price VARCHAR(40),pic VARCHAR(40),html VARCHAR(40))"
    try:
        cursor.execute(sql2)
        cursor.execute(sql) #执行操作语句
        db.commit() #提交到数据库执行
    except Exception as e:
        db.rollback() #发生错误回滚
        print("Error:\n",e) #打印异常
    db.close()

def getData(i,url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    # 因为是单页面，使用 select 方法获得的元素又是一个列表，那么列表中的第一个元素且也是唯一一个元素即是我们要找的信息 用 “[0]” 索引将其取出
    # 后在对其使用处理的方法，因为 beautifulsoup 的些筛选方法并不能针对列表类型的元素使用 ;)
    title = soup.select('div.pho_info > h4')[0].text.strip('\n')
    address = soup.select('div.pho_info > p')[0].get('title')
    """# 和 get('href') 同理，他们都是标签的一个属性而已，我们只需要的到这个属性的内容即可"""
    price = soup.select('div.day_l > span')[0].text
    pic = soup.select('#curBigImage')[0].get('src')
    """#“#”代表 id 这个找元素其实就是找他在页面的唯一"""
    host_name = soup.select('a.lorder_name')[0].text
    host_gender = soup.select('div.member_pic > div')[0].get('class')[0]

    # 根据结果观察不同性别会用不同的图标样式（class），设计一个函数进行转换
    def print_gender(class_name):
        if class_name == 'member_ico1':
            return '女'
        if class_name == 'member_ico':
            return '男'

    data = {
        'html': url,
        'title': title,
        'address': address,
        'price': price,
        'pic': pic,
        'host_name': host_name,
        'host_gender': print_gender(host_gender)
    }
    excel(i,data)
    Mysqlconnt(data)

# 如何批量获取链接
page_link = [] # <- 每个详情页的链接都存在这里，解析详情的时候就遍历这个列表然后访问就好啦~

def get_page_link(page_number):
    for each_number in range(6,page_number):
        full_url = 'http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(each_number)
        wb_data = requests.get(full_url)
        soup = BeautifulSoup(full_url)
        time.sleep(15)
        for link in soup.select('a.resule_img_a'):  # 找到这个 class 样为resule_img_a 的 a 标签即可
            page_link.append(link.get('href'))
        i = 0
        for htmlid in page_link:
            i+=1
            getData(i,htmlid)
            time.sleep(15)



#函数调用
get_page_link(20)


