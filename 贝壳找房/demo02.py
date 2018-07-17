import requests, codecs
import pymongo, time
from lxml import html
from pathos.multiprocessing import ProcessingPool as Pool


# 存储到MongoDB
# client = pymongo.MongoClient('mongodb://localhost:27017')
# db=client['testdb']
# myset=db['beike']
# 获取所有网址，打包成字典
def get_urldic():
    urllist = ['https://sh.zu.ke.com/zufang/jingan/',
               'https://sh.zu.ke.com/zufang/xuhui/',
               'https://sh.zu.ke.com/zufang/huangpu/',
               'https://sh.zu.ke.com/zufang/changning/',
               'https://sh.zu.ke.com/zufang/putuo/',
               'https://sh.zu.ke.com/zufang/pudong/',
               'https://sh.zu.ke.com/zufang/baoshan/',
               'https://sh.zu.ke.com/zufang/zhabei/',
               'https://sh.zu.ke.com/zufang/hongkou/',
               'https://sh.zu.ke.com/zufang/yangpu/',
               'https://sh.zu.ke.com/zufang/minhang/',
               'https://sh.zu.ke.com/zufang/jinshan/',
               'https://sh.zu.ke.com/zufang/jiading/',
               'https://sh.zu.ke.com/zufang/chongming/',
               'https://sh.zu.ke.com/zufang/fengxian/',
               'https://sh.zu.ke.com/zufang/songjiang/',
               'https://sh.zu.ke.com/zufang/qingpu/', ]
    pagenum = [21, 76, 39, 46, 50, 100, 100, 26, 31, 45, 100, 1, 63, 1, 19, 92, 44]
    urldic = dict(zip(urllist, pagenum))
    return urldic.keys(), urldic.values()


# 获取信息
def get_content(url1, pagenum):
    for j in range(1, pagenum):
        url = url1
        print('正在爬取{}第{}页,还剩{}页'.format(url, j, pagenum - j))
        url = url + 'pg' + str(j) + '/#contentList'
        r = requests.get(url)
        r = html.fromstring(r.text)
        lenth = len(r.xpath('//div[@class="content__article"]/div[1]/div'))
        try:
            for i in range(1, lenth + 1):
                urls = r.xpath('//div[@class="content__article"]/div[1]/div[{}]/div[1]/p[1]/a/@href'.format(i))[0]
                community = r.xpath('//div[@class="content__article"]/div[1]/div[{}]/div[1]/p[1]/a/text()'.format(i))[
                    0].replace('\n', '').strip()
                addr = r.xpath('//div[@class="content__article"]/div[1]/div[1]/div[{}]/p[2]/a/text()'.format(i))
                landlord = r.xpath('//div[@class="content__article"]/div[1]/div[{}]/div[1]/p[3]/text()'.format(i))[
                    0].replace('\n', '').strip()
                postime = r.xpath('//div[@class="content__article"]/div[1]/div[{}]/div[1]/p[4]/text()'.format(i))[0]
                label = r.xpath('//div[@class="content__article"]/div[1]/div[{}]/div[1]/p[5]/i/text()'.format(i))
                price = r.xpath('//div[@class="content__article"]/div[1]/div[{}]/div[1]/span/em/text()'.format(i))[0]
                output = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(url, community, addr, price, landlord, postime,
                                                                   label, urls)
                savetoexcel(output)
                # 如果是存储到MongoDB就用下面的
                # info={'community':community,'addr':addr,'price':price,'lanlord':landlord,'postime':postime,'label':label,'urls':urls}
                # try:
                #     myset.insert(info)
                # except:
                #     print('写入失败')

        except Exception as e:
            print(e)
            print('爬取失败')


# 保存到Excel
def savetoexcel(output):
    try:
        f = codecs.open('beike2.xls', 'a+')
        f.write(output)
        f.close()
    except Exception as e:
        print('写入失败')


# 主程序，开启多进程
if __name__ == '__main__':
    urldic = get_urldic()
    pool = Pool(processes=2)
    # 这里多进程传2个参数，所以用了pathos这个库
    pool.map(get_content, urldic[0], urldic[1])
    pool.close()
    pool.join()