import random
import scrapy
import logging

class proMiddleware(object):
    proxy_list = [
        "http://180.76.154.5:8888",
        "http://14.109.107.1:8998",
        "http://106.46.136.159:808",
        "http://175.155.24.107:808",
        "http://124.88.67.10:80",
        "http://124.88.67.14:80",
        "http://58.23.122.79:8118",
        "http://123.157.146.116:8123",
        "http://124.88.67.21:843",
        "http://106.46.136.226:808",
        "http://101.81.120.58:8118",
        "http://180.175.145.148:808"

    ]
    def process_request(self,request,spider):
        ip = random.choice(self.proxy_list)
        print(ip)
        request.meta['proxy'] = ip