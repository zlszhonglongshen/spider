#-*- coding: UTF-8 -*-

import urllib
import datetime

def download_stock_data(stock_list):
    for sid in stock_list:
        url = 'http://table.finance.yahoo.com/table.csv?s=' + sid

#侦测股票是否存在
        s = urllib.urlopen(url)
        code = s.getcode()
        if code !=200:
            print ("The %s 's record does not exist!" % (sid))
        continue


        fname = sid + '.csv'
        print('downloading %s from %s' % (fname,url))
        urllib.urlretrieve(url, fname)


def download_stock_data_period(stock_list,start,end):
#s为股票id
    for sid in stock_list:
        params = {'a': start.month - 1, 'b': start.day, 'c': start.year,
                  'd': end.month - 1, 'e': end.day, 'f': end.year, 's': sid}
        url = 'http://table.finance.yahoo.com/table.csv?'
        qs = urllib.urlencode(params)
        url = url + qs

# 侦测股票是否存在
        s = urllib.urlopen(url)
        code = s.getcode()
        if code != 200:
            print ("The %s's record does not exist!" %(sid))
            continue

        fname = '%s_%d%d%d_%d%d%d.csv' % (sid,start.year,start.month,start.day,end.year,end.month,end.day)
    print('downloading %s from %s' % (fname, url))
    urllib.urlretrieve(url, fname)


if __name__ == '__main__':
    stock_list = ['300001.sz', '300002.sz','600000.ss']
    end = datetime.date(year=2016,month=12,day=17)
    start = datetime.date(year=2016,month=11,day=17)
    download_stock_data_period(stock_list,start,end)
    download_stock_data(stock_list)