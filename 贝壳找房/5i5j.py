#coding:utf-8
import requests, codecs
import pymongo, time
from lxml import html
from multiprocessing import Pool


def get_content(j):
    print('正在爬取第{}页,还剩{}页'.format(j, 561 - j))
    url = 'https://sh.5i5j.com/xiaoqu/n{}/_?zn='.format(j)
    r = requests.get(url)
    r = html.fromstring(r.text)
    lenth = len(r.xpath('//ul[@class="pList"]/li'))
    try:
        for i in range(1, lenth):
            urls = r.xpath('//ul[@class="pList"]/li[{0}]/div[2]/h3/a/@href'.format(i))[0]
            community = r.xpath('//ul[@class="pList"]/li[{0}]/div[2]/h3/a/text()'.format(i))[0]
            deal = r.xpath('//ul[@class="pList"]/li[{0}]//div[2]/div[1]/p[1]/span[1]/a/text()'.format(i))[0]
            onsale = r.xpath('//ul[@class="pList"]/li[{0}]//div[2]/div[1]/p[1]/span[2]/a/text()'.format(i))[0].replace(
                '\r', '').replace('\n', '').strip()
            rent = r.xpath('//ul[@class="pList"]/li[{0}]//div[2]/div[1]/p[1]/span[3]/a/text()'.format(i))[0].replace(
                '\r', '').replace('\n', '').strip()
            # addr=r.xpath('//ul[@class="pList"]/li[{0}]/div[2]/div[1]/p[3]/text()'.format(i))[0].replace('\r','').replace('\n','').strip()
            avgprice = r.xpath('//ul[@class="pList"]/li[{0}]//div[2]/div[1]/div/p[1]/strong/text()'.format(i))[0]
            totalprice = r.xpath('//ul[@class="pList"]/li[{0}]//div[2]/div[1]/div/p[2]/text()'.format(i))[0]
            output = "{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(community, deal, onsale, rent, avgprice, totalprice, urls)
            savetoexcel(output)

    except Exception as e:
        print(e)
        print('爬取失败')


def savetoexcel(output):
    try:
        f = codecs.open('house.xls', 'a+', 'utf-8')
        f.write(output)
        f.close()
    except Exception as e:
        print('写入失败')


if __name__ == '__main__':
    pool = Pool(processes=2)
    pool.map(get_content, list(range(1, 561)))
    pool.close()
