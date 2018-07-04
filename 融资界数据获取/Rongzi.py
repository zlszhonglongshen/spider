# 导入第三方包
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# 设置请求头
headers = {'Accept':'*/*',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
          }


# 空列表，用于存储所有“详情”的链接
urls = []

# 遍历所有投资事件的网页，并抓下“详情”链接
for i in range(1,652):
    url = 'http://zdb.pedaily.cn/inv/p%s/' %i
    
    # 发送请求
    res = requests.get(url, headers = headers).text
    # 解析源代码
    soup = BeautifulSoup(res, 'html.parser')
    # 获取“详情”对应的url
    urls.extend(['http://zdb.pedaily.cn' + i.find('a')['href'] for i in soup.findAll('dt',{'class':'view'})[1:]])
    
# 先举一个链接中目标数据获取的例子
url = urls[0]
# 请求
res = requests.get(url, headers = headers).text
# 解析
soup = BeautifulSoup(res, 'html.parser')	
# 抓取目标字段
financing = soup.find('div',{'class':'info'}).findAll('li')[0].find('a').text
investment = soup.find('div',{'class':'info'}).findAll('li')[1].find('a').text
money = soup.find('div',{'class':'info'}).findAll('li')[2].text.split('：')[1]
turn = soup.find('div',{'class':'info'}).findAll('li')[3].text.split('：')[1]
date = soup.find('div',{'class':'info'}).findAll('li')[4].text.split('：')[1]
industry = soup.find('div',{'class':'info'}).findAll('li')[5].find('a').text	
# 打印结果
print(financing,investment,money,turn,date,industry)
	
	
# 通过循环，把所有链接的数据爬取下来
# 构建空列表，用户后面存储数据
data = []

# 循环抓数
for url in urls:
    # 获取源代码并解析
    res = requests.get(url, headers = headers).text
    soup = BeautifulSoup(res, 'html.parser')

    # 异常处理
    try:
        # 目标数据获取
        financing = soup.find('div',{'class':'info'}).findAll('li')[0].find('a').text
        investment = soup.find('div',{'class':'info'}).findAll('li')[1].find('a').text
        money = soup.find('div',{'class':'info'}).findAll('li')[2].text.split('：')[1]
        turn = soup.find('div',{'class':'info'}).findAll('li')[3].text.split('：')[1]
        date = soup.find('div',{'class':'info'}).findAll('li')[4].text.split('：')[1]
        industry = soup.find('div',{'class':'info'}).findAll('li')[5].find('a').text
    except:
        pass
    
    # 数据存储到字典中
    data.append({'financing':financing,'investment':investment,'money':money,'turn':turn,'date':date,'industry':industry})
	# 停顿，防止反爬
    time.sleep(3)
 
# 将抓取下来的信息构造成数据框对象 
Invest_Events = pd.DataFrame(data)

# 数据导出
Invest_Events.to_excel('Invest_Events.xlsx', index = False)