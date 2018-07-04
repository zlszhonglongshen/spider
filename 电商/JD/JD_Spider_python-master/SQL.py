#coding:utf-8
import MySQLdb as db

#将得到的数据存入数据库中mysql
class save_mysql:
    def __init__(self):
        self.user='root'
        self.password='root'
        self.host='127.0.0.1'
        self.database='mysql'
    def get_connection(self):
        return db.connect(user="root",passwd="root",host="127.0.0.1",db="mysql",charset="utf8mb4")

    def save_img(self,url):
        conn=self.get_connection()
        cursor=conn.cursor()
        cursor.execute("insert into JD(id,img_url) values(NULL,%s)",url)   #将img_url插入到数据库中
        conn.commit()
