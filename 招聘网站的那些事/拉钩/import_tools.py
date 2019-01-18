# spider.py
#-*-coding:utf-8-*-
import tools
import requests
import sys  
reload(sys)  
sys.setdefaultencoding('utf8') 

# 构造所有的url，并开始抓取（共30页）
for i in range(1,31):
    post_data = {'first':'true','kd':'python','pn': i}
    r = requests.post("http://www.lagou.com/jobs/positionAjax.json?px=default", data=post_data)
    html = r.text
    tools.fetch_content(html)
    