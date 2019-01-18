# coding:utf-8
import urllib2
import urllib
import re
import os
import shutil # 高效处理文件的模块

#sys为system的缩写，引入此模块是为了改变默认编码
import sys

reload(sys)
sys.setdefaultencoding('utf8')  #设置系统的编码为utf8，便于输入中文

host = 'http://www.dianping.com'
#自定义UA头部，直接用即可，不用理解细节
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'
headers = {'User-Agent':user_agent}
key_word = '齿科'                                      #写好要搜索的关键词
city_num = str(16)                                     #武汉的城市编码为16，其他城市的编码可以在点评网的URL中找到
directory = city_num + '\\' + unicode(key_word,'utf8')  #Windows系统下，创建中文目录名前需要制定编码，这里统一用UTF-8

if os.path.exists(directory):
    shutil.rmtree(directory)
    os.makedirs(directory)  #删除后再创建对应的关键词目录
    print ('delete existed directory successfully')
else:
    os.makedirs(directory)
    print ('create directory successfully')

url = host + '/search/keyword/' + city_num

def getDocument(page):
    page = str(page)
    path_name = directory + '\\page_' + page + '.txt'
    file = open(path_name, 'w+'); #创建文件

    #由于要搜索的关键词是中文，所以需要进行转码，这里调用了urllib.pathname2url函数
    real_url = url + '/' + '0_' + urllib.pathname2url(key_word) + '/p' + page
    request = urllib2.Request(real_url, headers = headers)                               #发送网络请求
    response = urllib2.urlopen(request)                                                  #得到网络响应
    document = response.read().encode('utf-8')                                           #将网页源码用UTF-8解码
    items_name = re.findall(r'data-hippo-type="shop"\stitle="([^"]+)"', document, re.S)  #正则匹配出商家名
    items_address = re.findall(r'<span\sclass="addr">([^\s]+)</span>', document, re.S)   #正则匹配出地址
    result = ''
    for index in range(len(items_name)):
        result += items_name[index] + '  ' + items_address[index] + '\n'
    file.write(result)                                                                   #将结果存入文件
    file.close()
    print ('Complete!')

def start_crawl():
    for index in range(0, 5):
        getDocument(index)


start_crawl()   #开始爬数据！