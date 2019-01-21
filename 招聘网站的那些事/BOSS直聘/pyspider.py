# -*- encoding: utf-8 -*-
# Project: BOSS
#https://blog.csdn.net/csdnnews/article/details/85822759   参考网址
 
from pyspider.libs.base_handler import *
import pymysql
import random
import time
import re
 
count = 0
 
class Handler(BaseHandler):
    # 添加请求头,否则出现403报错
    crawl_config = {'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}}
 
    def __init__(self):
        # 连接数据库
        self.db = pymysql.connect(host='127.0.0.1', user='root', password='774110919', port=3306, db='boss_job', charset='utf8mb4')
 
    def add_Mysql(self, id, job_title, job_salary, job_city, job_experience, job_education, company_name, company_type, company_status, company_people):
        # 将数据写入数据库中
        try:
            cursor = self.db.cursor()
            sql = 'insert into job(id, job_title, job_salary, job_city, job_experience, job_education, company_name, company_type, company_status, company_people) values ("%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (id, job_title, job_salary, job_city, job_experience, job_education, company_name, company_type, company_status, company_people);
            print(sql)
            cursor.execute(sql)
            print(cursor.lastrowid)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
 
    @every(minutes=24 * 60)
    def on_start(self):
        # 因为pyspider默认是HTTP请求,对于HTTPS(加密)请求，需要添加validate_cert=False,否则599/SSL报错
        self.crawl('https://www.zhipin.com/job_detail/?query=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&scity=100010000&industry=&position=', callback=self.index_page, validate_cert=False)
 
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        time.sleep(random.randint(2, 5))
        for i in response.doc('li > div').items():
            # 设置全局变量
            global count
            count += 1
            # 岗位名称
            job_title = i('.job-title').text()
            print(job_title)
            # 岗位薪水
            job_salary = i('.red').text()
            print(job_salary)
            # 岗位地点
            city_result = re.search('(.*?)<em class=', i('.info-primary > p').html())
            job_city = city_result.group(1).split(' ')[0]
            print(job_city)
            # 岗位经验
            experience_result = re.search('<em class="vline"/>(.*?)<em class="vline"/>', i('.info-primary > p').html())
            job_experience = experience_result.group(1)
            print(job_experience)
            # 岗位学历
            job_education = i('.info-primary > p').text().replace(' ', '').replace(city_result.group(1).replace(' ', ''), '').replace(experience_result.group(1).replace(' ', ''),'')
            print(job_education)
            # 公司名称
            company_name = i('.info-company a').text()
            print(company_name)
            # 公司类型
            company_type_result = re.search('(.*?)<em class=', i('.info-company p').html())
            company_type = company_type_result.group(1)
            print(company_type)
            # 公司状态
            company_status_result = re.search('<em class="vline"/>(.*?)<em class="vline"/>', i('.info-company p').html())
            if company_status_result:
                company_status = company_status_result.group(1)
            else:
                company_status = '无信息'
            print(company_status)
            # 公司规模
            company_people = i('.info-company p').text().replace(company_type, '').replace(company_status,'')
            print(company_people + '\n')
            # 写入数据库中
            self.add_Mysql(count, job_title, job_salary, job_city, job_experience, job_education, company_name, company_type, company_status, company_people)
        # 获取下一页信息
        next = response.doc('.next').attr.href
        if next != 'javascript:;':
            self.crawl(next, callback=self.index_page, validate_cert=False)
        else:
            print("The Work is Done")
        # 详情页信息获取,由于访问次数有限制,不使用
        #for each in response.doc('.name > a').items():
            #url = each.attr.href
            #self.crawl(each.attr.href, callback=self.detail_page, validate_cert=False)
 
    @config(priority=2)
    def detail_page(self, response):
        # 详情页信息获取,由于访问次数有限制,不使用
        message_job = response.doc('div > .info-primary > p').text()
        city_result = re.findall('城市：(.*?)经验', message_job)
        experience_result = re.findall('经验：(.*?)学历', message_job)
        education_result = re.findall('学历：(.*)', message_job)
 
        message_company = response.doc('.info-company > p').text().replace(response.doc('.info-company > p > a').text(),'')
        status_result = re.findall('(.*?)\d', message_company.split(' ')[0])
        people_result = message_company.split(' ')[0].replace(status_result[0], '')
 
        return {
            "job_title": response.doc('h1').text(),
            "job_salary": response.doc('.info-primary .badge').text(),
            "job_city": city_result[0],
            "job_experience": experience_result[0],
            "job_education": education_result[0],
            "job_skills": response.doc('.info-primary > .job-tags > span').text(),
            "job_detail": response.doc('div').filter('.text').eq(0).text().replace('\n', ''),
            "company_name": response.doc('.info-company > .name > a').text(),
            "company_status": status_result[0],
            "company_people": people_result,
            "company_type": response.doc('.info-company > p > a').text(),
        }
