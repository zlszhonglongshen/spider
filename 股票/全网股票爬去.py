import requests, re
from bs4 import BeautifulSoup


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''


# 获取股票编号的列表
def getStockList(stocklist, url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup('a', href=re.compile(r's[zh]\d{6}'))
    for i in a:
        try:
            href = i.attrs['href']
            id = re.findall(r's[zh]\d{6}', href)[0]
            stocklist.append(id)
        except:
            continue


# 获取股票信息
def getStockInfo(stockList, stockSearchUrl):
    count = 1
    for i in stockList:
        searchUrl = stockSearchUrl + i + '.html'
        html = getHTMLText(searchUrl)
        try:
            if html == '':
                continue

            soup = BeautifulSoup(html, 'html.parser')
            stockinfos = soup.find('div', attrs={'class': 'stock-bets'})
            stockDict = {}

            stockname = stockinfos.find_all(attrs={'class': 'bets-name'})[0]
            stockDict.update({'\n股票名称': stockname.text.split()[0]})

            keyList = stockinfos.find_all('dt')
            valueList = stockinfos.find_all('dd')

            for j in range(len(keyList)):
                key = keyList[j].text
                val = valueList[j].text
                stockDict[key] = val

            with open('股票信息.txt', 'a') as f:
                for k, v in stockDict.items():
                    f.write('\n\t{}:{}'.format(k, v))
                print("\r当前进度：{:.2f}".format(count * 100 / len(stockList)), end="")
                count += 1
        except:
            print("\r当前进度：{:.2f}%".format(count * 100 / len(stockList)), end="")
            count += 1
            continue


def main():
    stockListUrl = 'http://quote.eastmoney.com/stocklist.html'
    stockSearchUrl = 'https://gupiao.baidu.com/stock/'
    # 股票编号列表
    stockList = []
    getStockList(stockList, stockListUrl)
    getStockInfo(stockList, stockSearchUrl)


main()

