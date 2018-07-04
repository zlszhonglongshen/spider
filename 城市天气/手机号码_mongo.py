from bs4 import BeautifulSoup
import requests
import pymongo
import time

client = pymongo.MongoClient('localhost',27017)
data_58 = client['data_58']
shoujihao = data_58['shoujihao']

def get_data(url):
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text, 'lxml')
    no_longer_exist = soup.find('script', type="text/javascript").get('src')
    if no_longer_exist != None:
        pass
    else:
        url_links = soup.select('div.boxlist > ul > li > a')
        for url_link in url_links:
            if 'bj.58.com' in url_link.get('href'):
                if len(url_link.select('b.price')) > 0:
                    price = url_link.select('b.price')[0].get_text()
                else:
                    price = '面议'
                data = {
                    'title': url_link.select('strong')[0].get_text(),
                    'link': url_link.get('href').split('?')[0],
                    'price': price
                }
                print(data)
                shoujihao.insert_one(data)
#pages要爬取的页数
def main(pages):
    count = 0
    urls = ['http://bj.58.com/shoujihao/pn{}/'.format(str(i)) for i in range(0,pages+1)]
    for url in urls:
        get_data(url)
        print(count)
        count+=1
        time.sleep(2)

main(116)