from datetime import datetime
import requests
import json
import MySQLdb

#city表中拿到uid
conn=MySQLdb.connect(host='localhost',user='root',password='root',db='baidumap',charset='utf8')
cur=conn.cursor()
sql="Select uid from baidumap.city WHERE id>0;"
cur.execute(sql)
conn.commit()
uids=cur.fetchall()

##定义一个getjson函数用来解析返回的数据
def getjson(uid):
    try:
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        params={
            'uid':uid,
            'scope':'2',
            'output':'json',
            'ak':'XM53LMurtNQaAPFuKVy1WzSyZCNmNA9H',
        }
        url='http://api.map.baidu.com/place/v2/detail'
        response=requests.get(url=url,headers=headers,params=params)
        html=response.text
        decodejson=json.loads(html)
        return decodejson
    except:
        pass

#获取数据，存储数据
for uid in uids:
    uid=uid[0]
    print(uid)
    decodejson=getjson(uid)
    data=decodejson.get('result')
    if data:
        park=data.get('name')
        location_lat = data.get('location').get('lat')
        location_lng=data.get('location').get('lng')
        address=data.get('address')
        street_id=data.get('street_id')
        telephone=data.get('telephone')
        detail=data.get('detail')
        uid=data.get('uid')
        tag=data.get('detail_info').get('tag')
        detail_url=data.get('detail_info').get('detail_url')
        type=data.get('detail_info').get('type')
        overall_rating=data.get('detail_info').get('overall_rating')
        image_num=data.get('detail_info').get('image_num')
        comment_num=data.get('detail_info').get('comment_num')
        shop_hours=data.get('detail_info').get('shop_hours')
        alias=data.get('detail_info').get('alias')
        scope_type=data.get('detail_info').get('scope_type')
        scope_grade=data.get('detail_info').get('scope_grade')
        description=data.get('detail_info').get('description')
        sql="""INSERT INTO baidumap.park(park,location_lat,location_lng,address,street_id,telephone,
detail,uid,tag,detail_url,type,overall_rating,image_num,comment_num,shop_hours,alias,scope_type,scope_grade,
description,time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
        cur.execute(sql,(park,location_lat,location_lng,address,street_id,telephone,
detail,uid,tag,detail_url,type,overall_rating,image_num,comment_num,shop_hours,alias,scope_type,scope_grade,
description,datetime.now()))
        conn.commit()
cur.close()
conn.close()