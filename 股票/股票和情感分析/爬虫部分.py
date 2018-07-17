import re, requests, codecs, time, random
from lxml import html
from aip import AipNlp

# proxies={"http" : "123.53.86.133:61234"}
proxies = None
headers = {
    'Host': 'guba.eastmoney.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}


def get_url(page):
    stocknum = 600570
    url = 'http://guba.eastmoney.com/list,' + str(stocknum) + '_' + str(page) + '.html'
    try:
        text = requests.get(url, headers=headers, proxies=proxies, timeout=20)
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        text = html.fromstring(text.text)
        urls = text.xpath('//div[@id="articlelistnew"]/div[@class="articleh"]/span[3]/a/@href')
    except Exception as e:
        print(e)
        time.sleep(random.random() + random.randint(0, 3))
        urls = ''
    return urls


def get_comments(urls):
    for newurl in urls:
        newurl1 = 'http://guba.eastmoney.com' + newurl
        try:
            text1 = requests.get(newurl1, headers=headers, proxies=proxies, timeout=20)
            requests.adapters.DEFAULT_RETRIES = 5
            s = requests.session()
            s.keep_alive = False
            text1 = html.fromstring(text1.text)
            times1 = text1.xpath('//div[@class="zwli clearfix"]/div[3]/div/div[2]/text()')
            times = '!'.join(re.sub(re.compile('发表于| '), '', x)[:10] for x in times1).split('!')
            # times=list(map(lambda x:re.sub(re.compile('发表于| '),'',x)[:10],times))
            comments1 = text1.xpath('//div[@class="zwli clearfix"]/div[3]/div/div[3]/text()')
            comments = '!'.join(w.strip() for w in comments1).split('!')
            dic = dict(zip(times, comments))
            save_to_file(dic)
        except:
            print('error!!!!')
            time.sleep(random.random() + random.randint(0, 3))
        # print(dic)
        # if times and comments:
        # dic.append({'time':times,'comment':comments})
    # return dic


def save_to_file(dic):
    if dic:
        # dic=dic
        print(dic)
        # df=pd.DataFrame([dic]).T
        # df.to_excel('eastnoney.xlsx')
        for i, j in dic.items():
            output = '{}\t{}\n'.format(i, j)
            f = codecs.open('eastmoney.xls', 'a+', 'utf-8')
            f.write(output)
            f.close()


for page in range(2, 1257):
    print('正在爬取第{}页'.format(page))
    urls = get_url(page)
    dic = get_comments(urls)
