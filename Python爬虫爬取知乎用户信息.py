# -*- coding:utf-8 -*-
#https://blog.csdn.net/s291547/article/details/76213011
from bs4 import BeautifulSoup
import requests
import re
import pymysql
import threading
import queue
import time

#用于保存用户uid在数据库中序号的队列
q = queue.Queue(maxsize=3000)

conn_0 = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root',
                               db='zhihu', charset='utf8')

cursor_0 = conn_0.cursor()
#将未读取过的用户入列
sql_0 = 'SELECT order_number from infant_userid where is_read = 0'
cursor_0.execute(sql_0)
conn_0.commit()
for r in cursor_0:
    r = re.sub("\D", "", str(r))
    print(r)
    q.put(r)

class zhihu():
    def __init__(self):
        # 连接数据库
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='', passwd='',
                               db='zhihu', charset='utf8')
        self.main_url = 'https://www.zhihu.com/people/'
        self.answers_url = '/answers'
        self.topics_url = '/following/topics?page='
        self.asks_url = '/asks?page='
        self.question_url = 'https://www.zhihu.com/question/'
        self.headers = {
            "Host": "www.zhihu.com",
            "Referer": "https://www.zhihu.com/",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }

    def get_userinfo(self, user_token, proxies):
        # 获取用户名字
        url1 = self.main_url + user_token
        content = requests.get(url1, headers=self.headers, proxies=proxies).content
        #print(content.text)
        pattern = re.compile(r'<span class="ProfileHeader-name">(.+?)</span>')
        try:
            name_temp = pattern.findall(content.text)
        except:
            #除去僵尸用户，即未登陆无法查看信息的用户
            sql1 = "delete from infant_userid where token_id = '"+user_token+"'"
            self.cursor.execute(sql1)
            self.conn.commit()
            print(user_token+" is a ghost!!")
            pass
        else:
            print(name_temp)
            name = name_temp[0]
            print(name)
            # 获取用户关注的话题
            url2 = self.main_url + user_token + self.topics_url
            # print("fetching userinfo...")
            n = 1  # 话题的页数
            count = 21
            all_topics = []  # 用于存放话题的列表
            while count > 20:
                content = requests.get(url2 + str(n), headers=self.headers, proxies=proxies)
                pattern = re.compile(r'&quot;name&quot;:&quot;(.+?)&quot;')
                topics = pattern.findall(content.text)
                all_topics = all_topics + topics
                n = n + 1
                count = len(topics)
            all_topics = list(set(all_topics))  # 去重
            topics_str = ";".join(all_topics)  # 转字符串
            print(topics_str)

            # 链接数据库
            sql2 = "INSERT INTO infant_users (tokenID,username,topics) VALUES ('" + user_token + "','" + name + "','" + topics_str + "')"
            self.cursor.execute(sql2)
            # print(sql)
            self.get_question(user_token, proxies)

    def get_question(self, user_token, proxies):
            # 获取用户的提问
            url = self.main_url + user_token + self.asks_url
            #print(url)
            #print("fetching questions...")
            n = 1  # page
            question_count = 20
            while question_count > 19:
                content = requests.get(url + str(n), headers=self.headers, proxies=proxies)
                pattern = re.compile(r'&quot;http://www.zhihu.com/api/v4/questions/(.+?)&quot;')
                question_tokens = pattern.findall(content.text)
                # print(question_tokens)
                for question_token in question_tokens:
                    #print(question_token)
                    url2 = self.question_url + question_token
                    content2 = requests.get(url2, headers=self.headers, proxies=proxies).content
                    soup = BeautifulSoup(content2, 'lxml')
                    try:
                        title = soup.find('h1', attrs={'class', 'QuestionHeader-title'})
                    except:
                        #问题未登陆无法访问的情况
                        print('question is empty')
                        pass
                    else:
                        title = title.get_text()
                        print(title)
                        sql_tags = []
                        tags = soup.find_all('span', attrs={'class', 'Tag-content'})
                        for tag in tags:
                            tag = tag.get_text()
                            sql_tags.append(tag)
                        # print(sql_tags)
                        tags_str = ";".join(sql_tags)  # 转字符串

                        # 操作mysql
                        sql1 = "INSERT INTO infant_questions (questionsID,question,tags,askerID) VALUES ('" + question_token + "','" + title + "','" + tags_str + "','" + user_token + "')"
                        # print(sql1)
                        self.cursor.execute(sql1)
                        # time.sleep(0.5)

                # 页面计数加一
                n = n + 1
                question_count = len(question_tokens)
                # print(count)
            #print("fetch questions done")

    def run(self):
        count = 0
        while count < 100:
            if not (q.empty()):
                user_num = q.get()
                print(user_num)
                self.cursor = self.conn.cursor()
                sql = "SELECT token_id FROM infant_userid WHERE order_number='" + str(user_num) + "'"
                self.cursor.execute(sql)
                self.conn.commit()
                try:
                    user_token = self.cursor.fetchone()[0]
                except:
                    print("获取用户名出错，重试中...")
                    pass
                else:
                    print("feching the no." + str(user_num) + " user: " + user_token + "...")
                    # 代理，还需手动填入
                    proxies_pool = [{'https': 'https://210.43.38.251:8998'}, {'https': 'https://111.155.116.247:8123'}]
                    proxies_num = 1
                    proxies = []
                    #try:
                    self.get_userinfo(user_token, proxies)
                    #except:
                        #print("发生错误，重试中...")
                        #q.put(user_num)
                        #pass
                    #else:
                    sql2 = "UPDATE infant_userid SET is_read=1 where token_id='" + str(user_token) + "'"
                    self.cursor.execute(sql2)
                    self.conn.commit()
                    count += 1
                    print(count)
                print("fetch done")

        self.cursor.close()

if __name__ == "__main__":
    #定时重启的主线程
    for i in range(1, 10):
        #线程列表
        thread = []
        for i in range(0, 1):
            z = zhihu()
            t = threading.Thread(target=z.run, args=())
            #设为守护进程
            t.setDaemon(True)
            thread.append(t)
        for i in range(0, 1):
            thread[i].start()
        for i in range(0, 1):
            thread[i].join()
        time.sleep(1200)