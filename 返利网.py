# encoding=utf-8
import urllib2
from bs4 import BeautifulSoup
import time
# 返利网值得买页面的源代码中只包含5条数据，
# 其他的数据是动态加载的，每个页面包含50条数据

class FanLi():
    def __init__(self):
        self.user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers={'User-Agent':self.user_agent}
    def get_url(self):

        list_url=[]
        for i in range(1,760):
            # 可内容直接获取的url1
           url1='http://zhide.fanli.com/p'+str(i)
           list_url.append(url1)
           for j in range(2,11):
               url2='http://zhide.fanli.com/index/ajaxGetItem?cat_id=0&tag=&page='+str(i)+'-'+str(j)+'&area=0&tag_id=0&shop_id=0'
               list_url.append(url2)
        return list_url
    def getHtml(self,url):
        # url='http://zhide.fanli.com/p'+str(pageIndex)
        try:
            request=urllib2.Request(url,headers=self.headers)
            response=urllib2.urlopen(request)
            html=response.read()
            return html
        except urllib2.URLError,e:
            if hasattr(e,'reason'):
                print u"连接失败",e.reason
                return  None
    def parse(self):
        urls=self.get_url()
        i=0
        # with open('zhide.txt',a) as f:
        #     f.write()
        for url in urls:
            i=i+1
            html=self.getHtml(url)
            soup=BeautifulSoup(html,'html.parser')
            divs=soup.find_all('div',class_='zdm-list-item J-item-wrap item-no-expired')

            # for item in divs[0]:
            #     print 'item'+str(item)

            for div in divs:
                con_list=[]
                # 商品名称
                title=div.find('h4').get_text()
                # 分类
                item_type=div.find('div',class_='item-type').a.string
                # 推荐人
                item_user=div.find('div',class_='item-user').string
                # 内容
                item_cont=div.find('div',class_='item-content').get_text(strip=True)
                # 值得买人数
                type_yes=div.find('a',attrs={'data-type':'yes'}).string
                # 不值得买人数
                type_no=div.find('a',attrs={'data-type':'no'}).string
                con_list.append(title)
                con_list.append(item_type)
                con_list.append(item_user)
                con_list.append(item_cont)
                con_list.append(type_yes)
                con_list.append(type_no)


                f=open('zhide.txt','a')
                for item in con_list:
                    f.write(item.encode('utf-8')+'|')
                f.write('\n')
                f.close()
            print 'sleeping   loading %d'%i
            time.sleep(3)




zhide=FanLi()
zhide.parse()