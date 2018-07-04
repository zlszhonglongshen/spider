#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# 163mc.spider.py

from Crypto.Cipher import AES
import base64
import requests
import json
import codecs
import time

# 头部信息
headers = {
    'Accept':"*/*",
    'Accept-Encoding':"gzip, deflate",
    'Accept-Language':"zh-CN,zh;q=0.8",
    'Connection':"keep-alive",
    'Content-Length':"416",
    'Content-Type':"application/x-www-form-urlencoded",
    'Cookie':"_ntes_nnid=61528ed156a887c721f86bb28fb76864,1498012702495; _ntes_nuid=61528ed156a887c721f86bb28fb76864; playerid=72107504; JSESSIONID-WYYY=CBWAZVhlvjI8K2BH6zzZ%2Fg7D3eSt8d%2FBbX7cS%2FugonhTD4v%5CEMovRW%2FMMKaSSHsbxNWkASNlyqAs0kkNffuzVgNTeYe74hbWl3pCJPmdH3C5qpONJgrwkH9PNx1o6MOzdTdNKpYzw7HJZhbXXwAJ%2Fup%2F57wI2qFQTsvNi1rzWEr9vJug%3A1498075419550; _iuqxldmzr_=32; __utma=94650624.1764604869.1498012703.1498069886.1498074715.8; __utmb=94650624.3.10.1498074715; __utmc=94650624; __utmz=94650624.1498074715.8.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; MUSIC_U=0a56e5572596ab32367822d83962fb422c20eaf414934908a7ce96b1372782ad5962f7c16f34c1c6a337c009e727897da70b41177f9edcea; __remember_me=true; __csrf=880488a01f19e0b9f25a81842477c87b",
    'Host':"music.163.com",
    'Origin':"http://music.163.com",
    'Referer':"http://music.163.com/",
    'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
# 设置代理服务器
proxies= {
            'http:':'http://121.232.146.184',
            'https:':'https://144.255.48.197'
        }


# 第二个参数
second_param = "010001"
# 第三个参数
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
# 第四个参数
forth_param = "0CoJUm6Qyw8W8jud"

# 获取参数，page为传入页数
def get_params(page):
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    if(page == 1):
        # offset的取值为:(评论页数-1)*20,total第一页为true，其余页为false
        # first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}' # 第一个参数
        first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
        h_encText = AES_encrypt(first_param, first_key, iv)
    else:
        offset = str((page-1)*20)
        first_param = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' %(offset,'false')
        h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText

# 获取 encSecKey
def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


# 解密过程
def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text

# 获得评论json数据
def get_json(url, params, encSecKey):
    data = {
         "params": params,
         "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data,proxies = proxies)
    return response.content

# 抓取热门评论，返回热评列表
def get_hot_comments(url):
    hot_comments_list = []
    hot_comments_list.append(u"用户ID 用户昵称 用户头像地址 评论时间 点赞总数 评论内容\n")
    params = get_params(1) # 第一页
    encSecKey = get_encSecKey()
    json_text = get_json(url,params,encSecKey)
    json_dict = json.loads(json_text)
    hot_comments = json_dict['hotComments'] # 热门评论
    print("共有%d条热门评论!" % len(hot_comments))
    for item in hot_comments:
            comment = item['content'] # 评论内容
            likedCount = item['likedCount'] # 点赞总数
            comment_time = item['time'] # 评论时间(时间戳)
            userID = item['user']['userID'] # 评论者id
            nickname = item['user']['nickname'] # 昵称
            avatarUrl = item['user']['avatarUrl'] # 头像地址
            comment_info = userID + " " + nickname + " " + avatarUrl + " " + comment_time + " " + likedCount + " " + comment + u"\n"
            hot_comments_list.append(comment_info)
    return hot_comments_list

# 抓取某一首歌的全部评论
def get_all_comments(url):
    all_comments_list = [] # 存放所有评论
    all_comments_list.append(u"用户ID 用户昵称 用户头像地址 评论时间 点赞总数 评论内容\n") # 头部信息
    params = get_params(1)
    encSecKey = get_encSecKey()
    json_text = get_json(url,params,encSecKey)
    json_dict = json.loads(json_text)
    comments_num = int(json_dict['total'])
    if(comments_num % 20 == 0):
        page = comments_num / 20
    else:
        page = int(comments_num / 20) + 1
    print("共有%d页评论!" % page)
    for i in range(page):  # 逐页抓取
        params = get_params(i+1)
        encSecKey = get_encSecKey()
        json_text = get_json(url,params,encSecKey)
        json_dict = json.loads(json_text)
        if i == 0:
            print("共有%d条评论!" % comments_num) # 全部评论总数
        for item in json_dict['comments']:
            comment = item['content'] # 评论内容
            likedCount = item['likedCount'] # 点赞总数
            comment_time = item['time'] # 评论时间(时间戳)
            userID = item['user']['userId'] # 评论者id
            nickname = item['user']['nickname'] # 昵称
            avatarUrl = item['user']['avatarUrl'] # 头像地址
            comment_info = unicode(userID) + u" " + nickname + u" " + avatarUrl + u" " + unicode(comment_time) + u" " + unicode(likedCount) + u" " + comment + u"\n"
            all_comments_list.append(comment_info)
        print("第%d页抓取完毕!" % (i+1))
    return all_comments_list


# 将评论写入文本文件
def save_to_file(list,filename):
        with codecs.open(filename,'a',encoding='utf-8') as f:
            f.writelines(list)
        print("写入文件成功!")

if __name__ == "__main__":
    start_time = time.time() # 开始时间
    url = "http://music.163.com//weapi/v1/resource/comments/R_SO_4_28875120?csrf_token=90e04572eb42b040167323ec2fcdd79f"
    filename = u"小岁月太着急.txt"
    all_comments_list = get_all_comments(url)
    save_to_file(all_comments_list,filename)
    end_time = time.time() #结束时间
    print("程序耗时%f秒." % (end_time - start_time))