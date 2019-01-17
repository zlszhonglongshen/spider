#coding:utf-8
import urllib2
import time
import re
print(time.clock())
url = 'http://sz.lianjia.com/ershoufang/pg'
for x in range(101):
    finalUrl = url + str(x) + '/'
    res = urllib2.urlopen(finalUrl)
    content=res.read().decode('utf-8')
    result = re.findall(r'>.{1,100}?</div></div><div class="flood">',content)
    for i in result:
        print(i[0:-31].replace('</a>','').decode('utf-8'))
print(time.clock())