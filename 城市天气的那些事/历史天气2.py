# -*- coding=utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import numpy as np

# strYear = '2013'
site = " "  ##这里可以直接设定要爬取的地方的名字
strFile = site + '.csv'
f = open(strFile, 'w')
for strYear in np.arange(2013,2018):
    for month in range(1, 13):
        if (month < 10):
            strMonth = '0' + str(month)
        else:
            strMonth = str(month)
        strYearMonth = str(strYear) + str(strMonth)
        print("\nGetting data for month" + strYearMonth + "...", end='')

        url = "http://lishi.tianqi.com/"+site+"/" + strYearMonth + ".html"
        try:
            page = urllib.request.urlopen(url)
            # 创建BeautifulSoup对象
            soup = BeautifulSoup(page, "html.parser")
            weatherSet = soup.find(attrs={"class": "tqtongji2"})
            if (weatherSet == None):
                print("fail to get the page", end='')
                continue

            for line in weatherSet.contents:
                if (line.__class__.__name__ == 'NavigableString'): continue
                if (len(line.attrs) > 0): continue
                lis = line.findAll('li')
                strDate = lis[0].text
                highWeather = lis[1].text
                lowWeather = lis[2].text
                weather = lis[3].text
                windDirection = lis[4].text
                windPower = lis[5].text
                f.write(strDate + ',' + lowWeather + ',' + highWeather + ',' + weather + ',' +
                            windDirection + ',' + windPower + '\n')
                print("done", end='')
        except Exception as e:
            print("Error", e)

f.close()