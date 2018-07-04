# -*- coding:utf-8 -*-
'''
抓取豆瓣电影某部电影的评论
这里以《我不是潘金莲为例》
网址链接:https://movie.douban.com/subject/26630781/comments
为了抓取全部评论需要先进行登录
'''
from selenium import webdriver
import time
import codecs
import jieba
import jieba.analyse as analyse
from wordcloud import WordCloud
from scipy.misc import imread
from os import path

def get_douban_comments(url):
    comments_list = [] # 评论列表
    login_url = 'https://accounts.douban.com/login?source=movie'
    user_name = '1111111'  # 这里替换成你的豆瓣用户名
    password = '11111111'  # 这里替换成你的密码
    driver = webdriver.Firefox() # 启动Firefox()
    driver.get(login_url)
    driver.find_element_by_id('email').clear() # 清除输入框
    driver.find_element_by_id('email').send_keys(user_name) # 输入用户名
    driver.find_element_by_id('password').clear()
    driver.find_element_by_id('password').send_keys(password) # 输入密码
    captcha_field = raw_input('请打开浏览器输入验证码:') # 手动填入验证码
    driver.find_element_by_id('captcha_field').send_keys(captcha_field)
    driver.find_element_by_class_name('btn-submit').click() # 点击登录按钮
    time.sleep(5) # 等待跳转到登录之后的页面
    driver.get(url) # 定位到目标页面
    driver.implicitly_wait(3) # 智能等待3秒
    n = 501 # 页数
    count = 10000 # 评论数目
    while True:
        try:
            results = driver.find_elements_by_class_name('comment')
            for result in results:
                # author = result.find_elements_by_tag_name('a')[1].text # 作者
                # vote = result.find_element_by_class_name('comment-vote').find_element_by_tag_name('span').text # 赞同数目
                # time0 = result.find_element_by_class_name('comment-info').find_elements_by_tag_name('span')[1].text # 时间
                comment = result.find_element_by_tag_name('p').text # 评论内容
                comments_list.append(comment+u'\n')
                print u"查找到第%d个评论" % count
                count += 1
            driver.find_element_by_class_name('next').click() # 点击下一页
            print u'第%d页查找完毕!' % n
            n += 1
            time.sleep(4)
        except Exception,e:
            print e
            break
    with codecs.open('pjl_comment.txt','a',encoding='utf-8') as f:
        f.writelines(comments_list)
    print u"查找到第%d页,第%d个评论!" %(n,count)

# 得到所有关键词
def get_all_keywords(file_name):
    word_lists = [] # 关键词列表
    with codecs.open(file_name,'r',encoding='utf-8') as f:
        Lists = f.readlines() # 文本列表
        for List in Lists:
            cut_list = list(jieba.cut(List))
            for word in cut_list:
                word_lists.append(word)
    word_lists_set = set(word_lists) # 去除重复元素
    sort_count = []
    word_lists_set = list(word_lists_set)
    length = len(word_lists_set)
    print u"共有%d个关键词" % length
    k = 1
    for w in word_lists_set:
        sort_count.append(w+u':'+unicode(word_lists.count(w))+u"次\n")
        print u"%d---" % k + w+u":"+unicode(word_lists.count(w))+ u"次"
        k += 1
    with codecs.open('count_word.txt','w',encoding='utf-8') as f:
        f.writelines(sort_count)

def get_top_keywords(file_name):
    top_word_lists = [] # 关键词列表
    with codecs.open(file_name,'r',encoding='utf-8') as f:
        texts = f.read() # 读取整个文件作为一个字符串
        Result = analyse.textrank(texts,topK=20,withWeight=True,withFlag=True)
        n = 1
        for result in Result:
            print u"%d:" % n ,
            for C in result[0]: # result[0] 包含关键词和词性
                print C,u"  ",
            print u"权重:"+ unicode(result[1]) # 关键词权重
            n += 1

# 绘制词云
def draw_wordcloud():
   with codecs.open('pjl_comment.txt',encoding='utf-8') as f:
       comment_text = f.read()
   cut_text = " ".join(jieba.cut(comment_text)) # 将jieba分词得到的关键词用空格连接成为字符串
   d = path.dirname(__file__) # 当前文件文件夹所在目录
   color_mask = imread("F:/python2.7work/wordcloud/alice_color.png") # 读取背景图片
   cloud = WordCloud(font_path=path.join(d,'simsun.ttc'),background_color='white',mask=color_mask,max_words=2000,max_font_size=40)
   word_cloud = cloud.generate(cut_text) # 产生词云
   word_cloud.to_file("pjl_cloud.jpg")



if __name__ == '__main__':
    '''
    url = 'https://movie.douban.com/subject/26630781/comments?start=10581&limit=20&sort=new_score'
    get_douban_comments(url)
    file_name = 'pjl_comment.txt'
    get_top_keywords(file_name)
    '''
    draw_wordcloud()