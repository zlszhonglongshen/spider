#coding:utf-8
import requests
from bs4 import BeautifulSoup
import pymysql

print("链接mysql")
db = pymysql.connect(host="127.0.0.1",user="root",passwd="",db="mysql")
print("链接成功！！！")
cursor = db.cursor()
cursor.execute("drop table if exists color")
sql = """CREATE TABLE COLOR (
        Color CHAR(20) NOT NULL,
        Value CHAR(10),
        Style CHAR(50) )"""

cursor.execute(sql)
hdrs = {'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'}

url = "http://html-color-codes.info/color-names/"
r = requests.get(url,headers = hdrs)
soup = BeautifulSoup(r.content.decode('gbk','ignore'),'lxml')
trs = soup.find_all('tr')
for tr in trs:
    style = tr.get('style') #获取每个 tr标签里面的style属性
    tds = tr.find_all('td')
    td = [x for x  in tds]
    name = td[1].text.strip()
    hex = td[2].text.strip() #
    # print u'颜色: ' + name + u'颜色值: '+ hex + u'背景色样式: ' + style
    # print 'color: ' + name + '\tvalue: '+ hex + '\tstyle: ' + style
    insert_color = ("INSERT INTO COLOR(Color,Value,Style)" "VALUES(%s,%s,%s)")
    data_color = (name, hex, style)
    cursor.execute(insert_color, data_color)
    db.commit()
    print ('******完成此条插入!')
