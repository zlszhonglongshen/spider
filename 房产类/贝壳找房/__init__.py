#coding:utf-8
import pymongo
import requests, codecs
import pymongo, time
from lxml import html
from multiprocessing import Pool

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['local']
myset = db['beike']


def get_content(j):
    print('正在爬取第{}页,还剩{}页'.format(j, 100 - j))
    url = 'https://sh.zu.ke.com/zufang/pg{}/#contentList'.format(j)
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
            # output="{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(community,addr,price,landlord,postime,label,urls)
            # savetoexcel(output)
            info = {'community': community, 'addr': addr, 'price': price, 'lanlord': landlord, 'postime': postime,
                    'label': label, 'urls': urls}
            try:
                myset.insert(info)
            except:
                print('写入失败')

    except Exception as e:
        print(e)
        print('爬取失败')


def savetoexcel(output):
    try:
        f = codecs.open('beike.xls', 'a+', 'utf-8')
        f.write(output)
        f.close()
    except Exception as e:
        print('写入失败')


if __name__ == '__main__':
    pool = Pool(processes=2)
    pool.map(get_content, list(range(1, 101)))
    pool.close()
    pool.join()