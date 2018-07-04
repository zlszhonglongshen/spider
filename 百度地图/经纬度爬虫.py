#coding:utf-8
import json
from urllib.request import urlopen, quote
from sklearn.cluster import KMeans

'''
8579497 		1xLfxWEW10O8no0jZwbvIPfTPHtEiuOL 	服务端 		设置 删除
		8579496 		xPQ66HVmvOCr3et9nXAuUHDSYEGaSHnX 	服务端 		设置 删除
		8579495 		Wf3Mb6sTUnc7nyEC8QoZZew3OcZUt0Rz 	服务端 		设置 删除
		8579494 		d1nXMvMrLBO4GzkNxpsENHoGt7nBEM43 	服务端 		设置 删除
		8579493 		0edCw8wDEO5z09fs9lSPSeb4ggbqh0Mj 	服务端 		设置 删除
		8579492 		8aQ8mIvwp7qBeZ1cj4s0VriemTY5aF7g 	服务端 		设置 删除
		8579491 		R7V6zkGwByUrFkhajAIzAM8Tfi4A2o0e 	服务端 		设置 删除
		8579490 		Du8U9pvyzGehmk46prIPvvq8Rjiz6IAp 	服务端 		设置 删除
		8579489 		WeoG4x5KPs2NauhcgUvSg70lz4W14k5M 	服务端 		设置 删除
		8579488 		aUbyzRKiz1KFeODyojeVn5n76xV43b2U 	服务端 		设置 删除
		8579486 		IPcGnqTOO61Km9L8zVXqe8bXY0GDZcBV 	服务端 		设置 删除
		8579485 		buorqfEl4GhHGPK6FoUSemaNRj1BCoEZ 	服务端 		设置 删除  禁用
						T2n4LjBoW6oLxuhLxE7N36w55RHmReWP
						Qrc3aHbZdONvHowY7ZHXfQbB
						4ef1d4fe79be3dd28f51ea5336746862
						IC96AbO521APtmpsaR9xCMqo
						ZYwo3nLkop42NKOaay5r8KLl65eNB3p0

'''

url = 'http://api.map.baidu.com/geocoder/v2/'
output = 'json'
ak = 'R7V6zkGwByUrFkhajAIzAM8Tfi4A2o0e'
a=['北京','天津','石家庄','太原','呼和浩特','沈阳','大连','长春','哈尔滨','上海','南京','杭州','宁波','合肥','福州','厦门','南昌','济南','青岛','郑州','武汉','长沙','广州','深圳','南宁','海口','重庆','成都','贵阳','昆明','拉萨','西安','兰州','西宁','银川','乌鲁木齐']
for i in a:
     add = quote(i)
     uri = url + '?' + 'address=' + add  + '&output=' + output + '&ak=' + ak #百度地理编码API
     req = urlopen(uri)
     res = req.read().decode()
     temp = json.loads(res)
     print(temp)
     # print(temp['result']['location']['lng'],temp['result']['location']['lat'])#打印出经纬度