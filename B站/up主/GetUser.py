import requests,json,time
 
#获取用户信息类
class GetUser:
    def __init__(self,uid):
        self.uid = uid
 
    #获取用户信息
    def getUserInfo(self):
        url = 'http://space.bilibili.com/ajax/member/GetInfo'
        try:
            data = { 'mid': '{}'.format(self.uid) ,'_' : '1492863092419','csrf':'' }
            headers ={'Accept':'application/json, text/plain, */*',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-CN,zh;q=0.8',
                'Connection':'keep-alive',
                'Content-Length':'32',
                'Content-Type':'application/x-www-form-urlencoded',
                'Cookie':'UM_distinctid=15b9449b43c1-04dfdd66b40759-51462d15-1fa400-15b9449b43d83; fts=1492841510; sid=j4j61vah; purl_token=bilibili_1492841536; buvid3=30EA0852-5019-462F-B54B-1FA471AC832F28080infoc; rpdid=iwskokplxkdopliqpoxpw; _cnt_pm=0; _cnt_notify=0; _qddaz=QD.cbvorb.47xm5.j1t4z5yc; pgv_pvi=9558976512; pgv_si=s2784223232; _dfcaptcha=02d046fd3cc2bfd2ce6724f8b2185887; CNZZDATA2724999=cnzz_eid%3D1176255236-1492841785-http%253A%252F%252Fspace.bilibili.com%252F%26ntime%3D1492857985',
                'Host':'space.bilibili.com',
                'Origin':'http://space.bilibili.com',
                'Referer':'http://space.bilibili.com/{}/'.format(self.uid),
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
                'X-Requested-With':'XMLHttpRequest'}
            r = requests.post(url,headers = headers,data = data)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            self.text = json.loads(r.text)
        except:
            return None
 
    #返回SQL插入语句
    def getInsertSQLCode(self):
        t = self.text
        author = t['data']['name']
        sex = t['data']['sex']
        sign = t['data']['sign']
        fansNumber = t['data']['fans']
        watchNumber = t['data']['playNum']
        registerTime = time.ctime(float(t['data']['regtime']))
        birthday = t['data']['birthday']
        address = t['data']['place']
        icon = t['data']['face']
        link = 'http://space.bilibili.com/{}/#!/'.format(self.uid)
        sql = "insert into author_db(uid, author, sex, sign, fansNumber, watchNumber, registerTime, birthday, address, icon, link) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(self.uid,author,sex,sign,fansNumber,watchNumber,registerTime,birthday,address,icon,link)
        return sql