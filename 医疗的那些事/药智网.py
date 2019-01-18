# encoding=utf-8
from bs4 import  BeautifulSoup
import urllib2
import time
class YBZC():
    def __init__(self):
        self.user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers={'User-Agent':self.user_agent}
    def getHtml(self,pageIndex):
        try:
            url='http://db.yaozh.com/zhuce?p='+str(pageIndex)
            request=urllib2.Request(url,headers=self.headers)
            respone=urllib2.urlopen(request)
            html=respone.read()
            return html
        except urllib2.URLError,e:
            if hasattr(e,'reason'):
                print u"连接失败",e.reason
                return  None
    def getItems(self):
        for i in range(1,13):
            html=self.getHtml()
            soup=BeautifulSoup(html,"html.parser")
            tr_list=soup.find_all('tr')
            # 表格标题
            if i==1:
                for item  in tr_list[0]:
                    if item not in ['\n','\t',' ']:
                        with open('yaopinzhuce1030.txt','a') as f:
                            f.write(item.get_text(strip=True).encode('utf-8')+'|')
                #=========================2015-10-30================================
                # 第一次的时候是现将数据全部都取下来，等存入文件的时候再筛选，现在直接筛选再
                # 存入文件中，当时的时候并没有想到并且没有理解get_text()方法，这个也是
                # 代码不精简的原因。。。。
                #===================================================================
                # list_tit=[]
                # for ths in tr_list[0]:
                    # if ths.find('a'):
                #         for item in ths:
                #             if type(item)!=unicode:
                #                 list_tit.append(item.string)
                #     else:
                #         list_tit.append(ths.get_text(strip=True))
                # for item in list_tit:
                #     if item not in ['',' ','\n','\t']:
                #         with open('yaopinzhuce_new.txt','a') as f:
                #             f.write(item.encode('utf-8')+'|')
            # 表格内容
            f=open('yaopinzhuce1030.txt','a')
            for tr in tr_list[1:]:
                f.write('\n')
                for item in tr:
                    if item not in ['',' ','\n']:
                       if item.string==None:
                            f.write('None'+'|')
                       else:
                            f.write(item.string.encode('utf-8')+'|')

            f.close()
            print 'sleeping... pageloading %d/12' %i
            time.sleep(5)


spider=YBZC()
spider.getItems()