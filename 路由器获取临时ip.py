# -*- coding: utf-8 -*-
"""
Created on 2018/9/16 17:28
@author: Johnson
"""
import json
import requests
import time
LOGIN_PASSWORD = ''#登陆密码（加密后）
CONNECT_USERNAME = ''#拨号用户名
CONNECT_PASSWORD = ''#拨号密码
TRY_TIMES = 5#重试次数

url_cmd = ''
headers = {
	'Accept':'application/json, text/javascript, */*; q=0.01',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.9',
	'Connection':'keep-alive',
	'Content-Length':'54',
	'Content-Type':'application/json; charset=UTF-8',
	'Host':'192.168.1.1',
	'Origin':'http://192.168.1.1',
	'Referer':'http://192.168.1.1/',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest'
}

def login():
	url_login = 'http://192.168.1.1/'
	data = json.dumps({"method":"do","login":{"password":LOGIN_PASSWORD}})
	return requests.post(url_login, data=data, headers=headers)

def disconnect():
	data = json.dumps({"network":{"change_wan_status":{"proto":"pppoe","operate":"disconnect"}},"method":"do"})
	response = requests.post(url_cmd,data=data,headers=headers)
	return response
def test():
	try:
		response = requests.get('http://www.baidu.com')
		return response.status_code==200
	except Exception as e:
		return False
def reconnect():
	data = json.dumps({"protocol":{"wan":{"wan_type":"pppoe"},"pppoe":{"username":"02202758195","password":"123456"}},"method":"set"})
	response = requests.post(url_cmd,data=data,headers=headers)
	return response
def pr():
	print(url_cmd)
def main():
	global url_cmd
	now =  "time.strftime('%H:%M:%S',time.localtime(time.time()))"
	r = login()
	if json.loads(r.text).get('error_code')==0:
		token = json.loads(r.text).get('stok')
		url_cmd = 'http://192.168.1.1/stok='+token+'/ds'
		print(eval(now)+': login success')
	else:
		print(eval(now)+': login failed')
		return None
	response = disconnect()
	if json.loads(response.text).get('error_code')==0:
		print(eval(now)+': disconnect success')
	else:
		print(eval(now)+': disconnect failed')
	time.sleep(10)
	for i in range(TRY_TIMES+1):
		if test():
			print(eval(now)+': success to connect to network')
			break
		else:
			print(eval(now)+': faile to connect to network')
			reconnect()
if __name__ == '__main__':
	main()