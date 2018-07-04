import urllib.request
import json
from city import city
from province import province

choice=input('查询省份或直辖市的天气请输入1，查询某个城市的天气请输入2\n')
if (choice=='1'):
	provincename=input('你想查哪个省份或直辖市的天气?\n')
	provincecode=province.get(provincename)
	city={v:k for  k,v in city.items()}
	for citycode in range(int(provincecode)*10000+1,int(provincecode)*10000+2000):
		if (city.get(str(citycode))):
			url = ('http://www.weather.com.cn/data/cityinfo/%s.html'%str(citycode))
			content = urllib.request.urlopen(url).read()
			data = json.loads(content.decode())
			result = data['weatherinfo']
			str_temp = ('%s %s %s ~ %s') % (result['city'],result['weather'],result['temp1'],result['temp2'])
			print (str_temp)
		else:
			continue
elif (choice=='2'):
	cityname =input('你想查哪个城市的天气？\n')
	citycode = city.get(cityname)
	url = ('http://www.weather.com.cn/data/cityinfo/%s.html'%citycode)
	content = urllib.request.urlopen(url).read()
	data = json.loads(content.decode())
	result = data['weatherinfo']
	str_temp = ('%s %s %s ~ %s') % (result['city'],result['weather'],result['temp1'],result['temp2'])
	print (str_temp)

else:
	print('不合法的输入')