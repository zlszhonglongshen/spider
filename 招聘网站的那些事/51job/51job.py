# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 23:06:50 2018

@author: Johnson
"""

import urllib
from urllib.request import urlopen()
import re
import pymysql
import sqlite3
#import sys
#sys.setdefaultencoding('utf-8') #处理中文字体使用Unicode编码

i = 0 #统计爬取总条目
def url_input(url):
    """
    爬取网页源码html信息
    """
    get_html = urlopen(url)
    read_html = get_html.read()
    return read_html
    
def find_data(html):
    """
    用正则表达式获取需要的信息
    """
    reg = re.compile(r'class="t1 ">.*?<a target="_blank" title="(.*?)".*?<span class="t2"><a target="_blank" title="(.*?)".*?<span class="t3">(.*?)</span>.*?<span class="t4">(.*?)</span>.*?<span class="t5">(.*?)</span>',re.S)
    items = re.findall(reg,html)
    return items
    
def find_all_page(html):
    """
    从第一页获取总页数
    """
    reg = re.compile(r'<span class="td">(.*?)</span><input id="jump_page" class="mytxt" type="text" value="1"/>',re.S)
    page_all = re.findall(reg,html)
    num = re.sub("\D","",page_all[0])#从第5页中提取数字
    return num
    
def data_to_splite(job,company,address,wages,date,jobname):
    """
    将信息存储到数据库
    """
    db = pymysql.connect(host="localhost",
                       port=3306,
                       user="root",
                       passwd="",
                       db="mysql",
                       charset="utf8mb4")
    cursor = db.cursor()
    sql= "insert into '51job'(job,company,address,wages,date,jobname) values (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\");"%(job,company,address,wages,date,jobname)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print("ERROR",e)
    
def data_to_txt(str,jobname):
    """
    将信息存储到文本
    """
    with open(u"51job%s.txt"%(jobname),'a+') as f:
        f.write(str)
        


def print_items(data_items,jobname):
    """
    从正则匹配的列表中获取信息存储打印
    """
#    global i
    for data in data_items:
        job = data[0]
        company = data[1]
        address = data[2]
        wages = data[3]
        date = data[4]
#        i += 1
        str1 ="["+str(i)+"] "+ job+"--"+company+"--"+address+"--"+wages+"--"+date+"\n"
        data_to_txt(str1,jobname)#存到文本
#        data_to_sqlite( job, company, address, wages, date,jobname)#存到数据库
#        print(str1)
        
def urlformat(urlstart):
    """
    返回{}.html格式字符串
    """
    url = re.sub('1.html','{}.html',urlstart)
    return url
    

def get_page_html(page_num,urlstart):
    """
    输入中页数，返回每一页的url
    """
    list=[]
    for i in range(page_num):
        url = urlformat(urlstart)
        url = url.format(i)
        list.append(url)
    return list

def all_job_get():
    """
    输入多个职位名称以及第一页url批量抓取
    """
    urldict = [
        {
            'jobname': "python_人脸属性相关",
            'urlstart': 'http://search.51job.com/list/010000,000000,0000,00,9,99,Python%25E5%25BC%2580%25E5%258F%2591%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        },
        {
            'jobname': u"嵌入式",
            'urlstart': 'http://search.51job.com/list/010000,000000,0000,00,9,99,Python%25E5%25BC%2580%25E5%258F%2591%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        },
        {
            'jobname': u"云计算",
            'urlstart': 'http://search.51job.com/list/010000,000000,0000,00,9,99,%25E4%25BA%2591%25E8%25AE%25A1%25E7%25AE%2597,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        },
        {
            'jobname': u"机器学习",
            'urlstart': 'http://search.51job.com/list/010000,000000,0000,00,9,99,Python%25E5%25BC%2580%25E5%258F%2591%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        },
        {
            'jobname': u"人工智能",
            'urlstart': 'http://search.51job.com/list/010000,000000,0000,00,9,99,%25E6%259C%25BA%25E5%2599%25A8%25E5%25AD%25A6%25E4%25B9%25A0,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        },
        {
            'jobname': u"自动驾驶",
            'urlstart': 'http://search.51job.com/list/010000,000000,0000,00,9,99,%25E8%2587%25AA%25E5%258A%25A8%25E9%25A9%25BE%25E9%25A9%25B6,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        },
        {
            'jobname': u"北上广深python",
            'urlstart': 'http://search.51job.com/list/010000%252C040000%252C020000%252C030200,000000,0000,00,9,99,python_人脸属性相关,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        },
    ]
    
    for data in urldict:
        jobname = data['jobname']
        urlstart = data['urlstart']
        html = url_input(urlstart)
        all_page_num = int(find_all_page(html))
        print('++++%s+++++'%(all_page_num))
        urllist = get_page_html(all_page_num,urlstart)
        for url in urllist:
            html = url_input(url)
            data_items = find_data(html)
            print_items(data_items,jobname)
        i = 0 #批量抓取后换个职位重新计数

        
def one_job_get():
    """
    单个职位信息抓取
    """
    # jobname = "python_人脸属性相关"
    # urlstart = 'http://search.51job.com/list/010000,000000,0000,00,9,99,Python%25E5%25BC%2580%25E5%258F%2591%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    # jobname = u"嵌入式"
    # urlstart = 'http://search.51job.com/list/010000,000000,0000,00,9,99,%25E5%25B5%258C%25E5%2585%25A5%25E5%25BC%258F%25E5%25BC%2580%25E5%258F%2591,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    # jobname =u"云计算"
    # urlstart ='http://search.51job.com/list/010000,000000,0000,00,9,99,%25E4%25BA%2591%25E8%25AE%25A1%25E7%25AE%2597,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    # jobname =u"机器学习"
    # urlstart = 'http://search.51job.com/list/010000,000000,0000,00,9,99,%25E6%259C%25BA%25E5%2599%25A8%25E5%25AD%25A6%25E4%25B9%25A0,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    # jobname =u"人工智能"
    # urlstart = 'http://search.51job.com/list/010000,000000,0000,00,9,99,%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    # jobname =u"自动驾驶"
    # urlstart = 'http://search.51job.com/list/010000,000000,0000,00,9,99,%25E8%2587%25AA%25E5%258A%25A8%25E9%25A9%25BE%25E9%25A9%25B6,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    #jobname =u"北上广深python"
    #urlstart = 'http://search.51job.com/list/010000%252C040000%252C020000%252C030200,000000,0000,00,9,99,python,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    jobname = u"BJ技术支持"
    urlstart = 'http://search.51job.com/list/010000,000000,0000,00,9,99,%25E6%258A%2580%25E6%259C%25AF%25E6%2594%25AF%25E6%258C%2581,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='

    html = url_input(urlstart)#获取首页
    all_page_num = int(find_all_page(html))#从首页获取总共页数
    print("+++++++++++++++++%s++++++++++++++++++++" % (all_page_num))
    urllist = get_page_html(all_page_num, urlstart)#获取每一页url存到列表里
    for url in urllist:#从列表里迭代每一页url
        html = url_input(url)#获取页面url
        data_items = find_data(html)#查找信息返回职位等信息
        print_items(data_items, jobname)#将信息存到文本信息和数据库

    
    
    
if __name__=='__main__':
    one_job_get()


      
    
    