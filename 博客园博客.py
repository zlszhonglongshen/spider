#coding:utf-8
# import urllib.parse
# import urllib.request
#
# # params  CategoryId=808 CategoryType=SiteHome ItemListActionName=PostList PageIndex=3 ParentCategoryId=0 TotalPostCount=4000
# def getHtml(url,values):
#     user_agent='Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
#     headers = {'User-Agent':user_agent}
#     data = urllib.parse.urlencode(values)
#     response_result = urllib.request.urlopen(url+'?'+data).read()
#     html = response_result.decode('utf-8')
#     return html
#
# #获取数据
# def requestCnblogs(index):
#     print('请求数据')
#     url = 'http://www.cnblogs.com/mvc/AggSite/PostList.aspx'
#     value= {
#          'CategoryId':808,
#          'CategoryType' : 'SiteHome',
#          'ItemListActionName' :'PostList',
#          'PageIndex' : index,
#          'ParentCategoryId' : 0,
#         'TotalPostCount' : 4000
#     }
#     result = getHtml(url,value)
#     return result

from bs4 import BeautifulSoup
import request
import re

#解析最外层
def blogParser(index):

  cnblogs = request.requestCnblogs(index)
  soup = BeautifulSoup(cnblogs, 'html.parser')
  all_div = soup.find_all('div', attrs={'class': 'post_item_body'}, limit=20)

  blogs = []
  #循环div获取详细信息
  for item in all_div:
      blog = analyzeBlog(item)
      blogs.append(blog)

  return blogs

#解析每一条数据
def analyzeBlog(item):
    result = {}
    a_title = find_all(item,'a','titlelnk')
    if a_title is not None:
        # 博客标题
        result["title"] = a_title[0].string
        # 博客链接
        result["href"] = a_title[0]['href']
    p_summary = find_all(item,'p','post_item_summary')
    if p_summary is not None:
        # 简介
        result["summary"] = p_summary[0].text
    footers = find_all(item,'div','post_item_foot')
    footer = footers[0]
    # 作者
    result["author"] = footer.a.string
    # 作者url
    result["author_url"] = footer.a['href']
    str = footer.text
    time = re.findall(r"发布于 .+? .+? ", str)
    result["create_time"] = time[0].replace('发布于 ','')

    comment_str = find_all(footer,'span','article_comment')[0].a.string
    result["comment_num"] = re.search(r'\d+', comment_str).group()

    view_str = find_all(footer,'span','article_view')[0].a.string
    result["view_num"] = re.search(r'\d+', view_str).group()

    return result

def find_all(item,attr,c):
    return item.find_all(attr,attrs={'class':c},limit=1)


import match
import os
import datetime
import json

def writeToTxt(list_name,file_path):
    try:
        #这里直接write item 即可，不要自己给序列化在写入，会导致json格式不正确的问题
        fp = open(file_path,"w+",encoding='utf-8')
        l = len(list_name)
        i = 0
        fp.write('[')
        for item in list_name:
            fp.write(item)
            if i<l-1:
                fp.write(',\n')
            i += 1
        fp.write(']')
        fp.close()
    except IOError:
        print("fail to open file")

#def getStr(item):
#   return json.dumps(item).replace('\'','\"')+',\n'

def saveBlogs():
    for i in range(1,2):
        print('request for '+str(i)+'...')
        blogs = match.blogParser(i,5)
        #保存到文件
        path = createFile()
        writeToTxt(blogs,path+'/blog_'+ str(i) +'.json')
        print('第'+ str(i) +'页已经完成')
    return 'success'

def createFile():
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    path = '/'+date
    if os.path.exists(path):
        return path
    else:
        os.mkdir(path)
        return path

result = saveBlogs()
print(result)