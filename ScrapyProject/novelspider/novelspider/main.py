#coding=utf-8
from scrapy import cmdline      # 导入命令行
cmdline.execute("scrapy crawl novspider".split())   #命令行运行scrapy工程

# 注意：crawl后的（这里novspider）是自己定义的 name (spider标识)的名字，不是工程名字