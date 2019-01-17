#coding:utf-8
# 导入开发模块
import requests
from bs4 import BeautifulSoup

# 定义空列表，用于创建所有的爬虫链接
urls = []
# 指定爬虫所需的上海各个区域名称
citys = ['pudongxinqu', 'minhang', 'baoshan', 'xuhui', 'putuo', 'yangpu', 'changning', 'songjiang',
         'jiading', 'huangpu', 'jinan', 'zhabei', 'hongkou', 'qingpu', 'fengxian', 'jinshan', 'chongming']

# 基于for循环，构造完整的爬虫链接
for i in citys:
    url = 'http://sh.lianjia.com/ershoufang/%s/' % i
    res = requests.get(url)  # 发送get请求
    res = res.text.encode(res.encoding).decode('utf-8')  # 需要转码，否则会有问题
    soup = BeautifulSoup(res, 'html.parser')  # 使用bs4模块，对响应的链接源代码进行html解析
    page = soup.findAll('div', {'class': 'page-box house-lst-page-box'})  # 使用finalAll方法，获取指定标签和属性下的内容
    pages = [i.strip() for i in page[0].text.split('\n')]  # 抓取出每个区域的二手房链接中所有的页数
    if len(pages) > 3:
        total_pages = int(pages[-3])
    else:
        total_pages = int(pages[-2])

    for j in list(range(1, total_pages + 1)):  # 拼接所有需要爬虫的链接
        urls.append('http://sh.lianjia.com/ershoufang/%s/d%s' % (i, j))

# 创建csv文件，用于后面的保存数据
file = open('lianjia.csv', 'w', encoding='utf-8')

for url in urls:  # 基于for循环，抓取出所有满足条件的标签和属性列表，存放在find_all中
    res = requests.get(url)
    res = res.text.encode(res.encoding).decode('utf-8')
    soup = BeautifulSoup(res, 'html.parser')
    find_all = soup.find_all(name='div', attrs={'class': 'info-panel'})

    for i in list(range(len(find_all))):  # 基于for循环，抓取出所需的各个字段信息
        title = find_all[i].find('a')['title']  # 每套二手房的标语

        res2 = find_all[i]
    name = res2.find_all('div', {'class': 'where'})[0].find_all('span')[0].text  # 每套二手房的小区名称
    room_type = res2.find_all('div', {'class': 'where'})[0].find_all('span')[1].text  # 每套二手房的户型
    size = res2.find_all('div', {'class': 'where'})[0].find_all('span')[2].text[:-3]  # 每套二手房的面积

    # 采用列表解析式，删除字符串的首位空格
    info = [i.strip() for i in res2.find_all('div', {'class': 'con'})[0].text.split('\n')]
    region = info[1]  # 每套二手房所属的区域
    loucheng = info[2][2:]  # 每套二手房所在的楼层
    chaoxiang = info[5][2:]  # 每套二手房的朝向
    builtdate = info[-3][2:]  # 每套二手房的建筑时间

    # 每套二手房的总价
    price = find_all[i].find('div', {'class': 'price'}).text.strip()[:-1]
    # 每套二手房的平方米售价
    price_union = find_all[i].find('div', {'class': 'price-pre'}).text.strip()[:-3]

    # print(name,room_type,size,region,loucheng,chaoxiang,price,price_union,builtdate)
    # 将上面的各字段信息值写入并保存到csv文件中
    file.write(','.join((name, room_type, size, region, loucheng, chaoxiang, price, price_union, builtdate)) + '\n')

# 关闭文件（否则数据不会写入到csv文件中）
file.close()