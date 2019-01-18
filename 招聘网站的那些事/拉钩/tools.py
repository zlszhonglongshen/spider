# tools.py
#-*-coding:utf-8-*-
import time,os,cookielib,urllib2,urllib
import StringIO,gzip

f = open('e:/data.txt','wb')

def write(positionName,companyShortName,city,workYear,positionAdvantage,salary,education,financeStage):
    f.write(positionName)
    f.write('\r\n')
    f.write(companyShortName)
    f.write('\r\n')
    f.write(city)
    f.write('\r\n')
    f.write(workYear)
    f.write('\r\n')
    f.write(positionAdvantage)
    f.write('\r\n')
    f.write(salary)
    f.write('\r\n')
    f.write(education)
    f.write('\r\n')
    f.write(financeStage)
    f.write('\r\n')
    f.write('\r\n')


def fj_function(url_content,beg_str,end_str,lengths):
    str_len=len(beg_str)
    start=url_content.find(beg_str,0,lengths)
    obj=''
    if start>=0:
        content=url_content[start+str_len:lengths]
        if end_str<>'':
            end=content.find(end_str,0,lengths)
            obj=content[0:end]
            content=content[end:lengths]
    else:
        content=url_content
    return content,obj


def fetch_content(url_content):
    lengths=len(url_content)
    while 1:
        beg_str = '"positionId"'
        str_len=len(beg_str)
        start=url_content.find(beg_str,0,lengths)
        if start>=0:
            url_content=url_content[start+str_len:lengths]
            end_str = '"positionId"'
            end=url_content.find(end_str,0,lengths)
            obj_content=url_content[:end]
            # 分拣具体数据
            obj_content,positionName=fj_function(obj_content,'"positionName":"','"',lengths) 
            obj_content,companyShortName=fj_function(obj_content,'companyShortName":"','"',lengths)
            obj_content,city=fj_function(obj_content,'"city":"','"',lengths)
            obj_content,workYear=fj_function(obj_content,'workYear":"','"',lengths)
            obj_content,positionAdvantage=fj_function(obj_content,'positionAdvantage":"','"',lengths)
            obj_content,salary=fj_function(obj_content,'salary":"','"',lengths)
            obj_content,education=fj_function(obj_content,'education":"','"',lengths)
            obj_content,financeStage=fj_function(obj_content,'financeStage":"','"',lengths)
            # 写入文件
            write(positionName,companyShortName,city,workYear,positionAdvantage,salary,education,financeStage)   
        else:
            break