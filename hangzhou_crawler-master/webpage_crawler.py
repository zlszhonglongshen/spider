# -*- coding: utf-8 -*-

import os
import re
import glob
import json
import time
import random
import urllib
import urllib2
import fileinput

headers = {'Connection':'keep-alive',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
'Referer':'http://hz.ganji.com/xiaoqu/o2/',
'Cookie':''}

file = open("ganji_xiaoqu.txt","w")
for i in xrange(100):
    print i
    url = "http://hz.ganji.com/xiaoqu/o2/f"+str(20*i)
    result = re.sub(' +', ' ', urllib2.urlopen(urllib2.Request(url, headers=headers)).read().replace("\n",""))
    for line in re.findall('<li class="list-img list-xq clearfix" >(.*?)</li>', result):
        urlp = re.findall('href="(.*?)"', line)[0]
        num1 = re.findall('ershoufang/" title="" target="_blank">(.*?)</a>', line)[0]
        num2 = re.findall('chuzufang/" title="" target="_blank">(.*?)</a>', line)[0]
        price = re.findall('<b class="fc-org xq-price-num">(.*?)</b>', line)[0]
        file.write(urlp+"\t"+num1+"\t"+num2+"\t"+price+"\n")
        print urlp, num1, num2, price
    time.sleep(random.uniform(0, 5))
file.close()

urls = []
for url in fileinput.input("ganji_xiaoqu.txt"):
    url = url.split("\t")[0].strip()
    urls.append(url)
file = open("ganji_xiaoqu_info.txt","a")
for i in range(0,2000):
    url = "http://hz.ganji.com/"+urls[i]
    result = re.sub(' +', ' ', urllib2.urlopen(urllib2.Request(url, headers=headers)).read().replace("\n","").replace("\t","").replace("&nbsp;",""))
    title = re.findall('<h1 class="xiaoqu-title">(.*?)</h1>', result)[0]
    price = re.findall('<b class="basic-info-price">(.*?)</b>', result)[0]
    num1 = re.sub('<.*?>', '', re.findall('二手房：(.*?)</a>', result)[0])
    num2 = re.sub('<.*?>', '', re.findall('出租房：(.*?)</a>', result)[0])
    stime = re.findall('竣工时间：</span>(.*?)</li>', result)[0]
    s1 = re.findall('容积率：</i>(.*?)<i class="ico_ask"', result)[0].strip()
    s2 = re.findall('绿化率：</i>(.*?)<i class="ico_ask"', result)[0].strip()
    s3 = re.findall('物业费：</dt> <dd class="fl"> <div>(.*?)</div>', result)[0].strip()
    near = re.sub('<.*?>', '', re.findall('周边配套：</dt> <dd class="fl">(.*?)</dd>', result)[0])
    poi = re.findall('"lnglat":"b(.*?)"', result)[0] if len(re.findall('"lnglat":"b(.*?)"', result)) >= 1 else "0"
    a1 = re.sub('<.*?>', ' ', re.findall('<li>一居(.*?)</li>', result)[0]).replace("(","").replace(")","").replace(" ","") if len(re.findall('<li>一居(.*?)</li>', result)) >= 1 else "0套"
    a2 = re.sub('<.*?>', ' ', re.findall('<li>二居(.*?)</li>', result)[0]).replace("(","").replace(")","").replace(" ","") if len(re.findall('<li>二居(.*?)</li>', result)) >= 1 else "0套"
    a3 = re.sub('<.*?>', ' ', re.findall('<li>三居(.*?)</li>', result)[0]).replace("(","").replace(")","").replace(" ","") if len(re.findall('<li>三居(.*?)</li>', result)) >= 1 else "0套"
    a4 = re.sub('<.*?>', ' ', re.findall('<li>四居(.*?)</li>', result)[0]).replace("(","").replace(")","").replace(" ","") if len(re.findall('<li>四居(.*?)</li>', result)) >= 1 else "0套"
    a5 = re.sub('<.*?>', ' ', re.findall('<li>五居(.*?)</li>', result)[0]).replace("(","").replace(")","").replace(" ","") if len(re.findall('<li>五居(.*?)</li>', result)) >= 1 else "0套"
    a0 = re.sub('<.*?>', ' ', re.findall('<li>其他居(.*?)</li>', result)[0]).replace("(","").replace(")","").replace(" ","") if len(re.findall('<li>其他居(.*?)</li>', result)) >= 1 else "0套"
    b1 = re.sub('<.*?>', ' ', re.findall('<li>30万以下(.*?)</li>', result)[0]).replace("(","").replace(")","").replace(" ","") if len(re.findall('<li>30万以下(.*?)</li>', result)) >= 1 else "0套"
    b2 = re.sub('<.*?>', ' ', re.findall('<li>30-60万(.*?)</li>', result)[0]).replace("(","").replace(")","").replace(" ","") if len(re.findall('<li>30-60万(.*?)</li>', result)) >= 1 else "0套"
    b3 = re.sub('<.*?>', ' ', re.findall('<li>60-100万(.*?)</li>', result)[0]).replace("(","").replace(")","").replace(" ","") if len(re.findall('<li>60-100万(.*?)</li>', result)) >= 1 else "0套"
    b4 = re.sub('<.*?>', ' ', re.findall('<li>100-150万(.*?)</li>', result)[0]).replace("(","").replace(")","").replace(" ","") if len(re.findall('<li>100-150万(.*?)</li>', result)) >= 1 else "0套"
    b5 = re.sub('<.*?>', ' ', re.findall('<li>150-200万(.*?)</li>', result)[0]).replace("(","").replace(")","").replace(" ","") if len(re.findall('<li>150-200万(.*?)</li>', result)) >= 1 else "0套"
    b6 = re.sub('<.*?>', ' ', re.findall('<li>200万以上(.*?)</li>', result)[0]).replace("(","").replace(")","").replace(" ","") if len(re.findall('<li>200万以上(.*?)</li>', result)) >= 1 else "0套"
    c1 = re.sub('<.*?>', ' ', re.findall('<li>整租(.*?)</li>', result)[0]).replace("(","").replace(")","").replace(" ","") if len(re.findall('<li>整租(.*?)</li>', result)) >= 1 else "0套"
    c2 = re.sub('<.*?>', ' ', re.findall('<li>合租(.*?)</li>', result)[0]).replace("(","").replace(")","").replace(" ","") if len(re.findall('<li>合租(.*?)</li>', result)) >= 1 else "0套"
    print i, poi
    file.write(urls[i]+"\t"+title+"\t"+price+"\t"+num1+"\t"+num2+"\t"+stime+"\t"+s1+"\t"+s2+"\t"+s3+"\t"+near+"\t"+poi+"\t"+a1+"\t"+a2+"\t"+a3+"\t"+a4+"\t"+a5+"\t"+a0+"\t"+b1+"\t"+b2+"\t"+b3+"\t"+b4+"\t"+b5+"\t"+b6+"\t"+c1+"\t"+c2+"\n")
    time.sleep(random.uniform(0, 3))
file.close()

exist = {}
for line in fileinput.input("ganji_xiaoqu_unit.txt"):
    exist[line.split("\t")[0]] = True
file = open("ganji_xiaoqu_unit.txt","a")
for line in fileinput.input("ganji_xiaoqu.txt"):
    name, num1, num2 = line.split("\t")[0], int(line.split("\t")[1]), int(line.split("\t")[2])
    if not exist.has_key(name):
        if num1 > 0:
            for i in xrange(num1/20+1):
                url = "http://hz.ganji.com/"+name+"ershoufang/f"+str(20*i)
                result = re.sub(' +', ' ', urllib2.urlopen(urllib2.Request(url, headers=headers)).read().replace("\n","").replace("\t","").replace("&nbsp;",""))
                title = re.findall('<h3 class="xiaoqu-title">(.*?)</h3>', result)[0]
                basic = [re.sub('<.*?>', '', item) for item in re.findall('<p class="list-word pt-4">(.*?)</p>', result)]
                price = re.findall('<b class="fc-org f16">(.*?)</b>', result)
                for u in xrange(len(basic)):
                    file.write(name+"\t"+"ershou"+"\t"+title+"\t"+basic[u]+"\t"+price[u]+"\n")
                time.sleep(random.uniform(0, 3))
        if num2 > 0:
            for i in xrange(num2/20+1):
                url = "http://hz.ganji.com/"+name+"chuzufang/f"+str(20*i)
                result = re.sub(' +', ' ', urllib2.urlopen(urllib2.Request(url, headers=headers)).read().replace("\n","").replace("\t","").replace("&nbsp;",""))
                title = re.findall('<h3 class="xiaoqu-title">(.*?)</h3>', result)[0]
                basic = [re.sub('<.*?>', '', item) for item in re.findall('<p class="list-word pt-4">(.*?)</p>', result)]
                price = re.findall('<b class="fc-org f16">(.*?)</b>', result)
                for u in xrange(len(basic)):
                    file.write(name+"\t"+"chuzu"+"\t"+title+"\t"+basic[u]+"\t"+price[u]+"\n")
                time.sleep(random.uniform(0, 3))
    else:
        print "exist"
        continue
file.close()

glist = [
"http://www.wealink.com/gongsi/hangzhou_jisuanjiruanjian_o5",
"http://www.wealink.com/gongsi/hangzhou_jisuanjiyingjian_o5",
"http://www.wealink.com/gongsi/hangzhou_jisuanjifuwu_o5",
"http://www.wealink.com/gongsi/hangzhou_tongxin_o5",
"http://www.wealink.com/gongsi/hangzhou_dianxin_o5",
"http://www.wealink.com/gongsi/hangzhou_hulianwang_o5",
"http://www.wealink.com/gongsi/hangzhou_wangluoyouxi_o5",
"http://www.wealink.com/gongsi/hangzhou_dianzijishu_o5",
"http://www.wealink.com/gongsi/hangzhou_yiqiyibiao_o5",
"http://www.wealink.com/gongsi/hangzhou_shenji_o5",
"http://www.wealink.com/gongsi/hangzhou_jinrongtouzi_o5",
"http://www.wealink.com/gongsi/hangzhou_yinhang_o5",
"http://www.wealink.com/gongsi/hangzhou_baoxian_o5",
"http://www.wealink.com/gongsi/hangzhou_ad_o5",
"http://www.wealink.com/gongsi/hangzhou_gongguan_o5",
"http://www.wealink.com/gongsi/hangzhou_yingshi_o5",
"http://www.wealink.com/gongsi/hangzhou_wenzimeiti_o5",
"http://www.wealink.com/gongsi/hangzhou_yinshua_o5",
"http://www.wealink.com/gongsi/hangzhou_zhongjiefuwu_o5",
"http://www.wealink.com/gongsi/hangzhou_zhuanyefuwu1_o5",
"http://www.wealink.com/gongsi/hangzhou_waibaofuwu_o5",
"http://www.wealink.com/gongsi/hangzhou_jiance_o5",
"http://www.wealink.com/gongsi/hangzhou_falv_o5",
"http://www.wealink.com/gongsi/hangzhou_jiaoyu_o5",
"http://www.wealink.com/gongsi/hangzhou_xueshu_o5",
"http://www.wealink.com/gongsi/hangzhou_zhiyao_o5",
"http://www.wealink.com/gongsi/hangzhou_yiliaohuli_o5",
"http://www.wealink.com/gongsi/hangzhou_yiliaoshebei_o5",
"http://www.wealink.com/gongsi/hangzhou_fangdichan_o5",
"http://www.wealink.com/gongsi/hangzhou_jianzhujiancai_o5",
"http://www.wealink.com/gongsi/hangzhou_sheneisheji_o5",
"http://www.wealink.com/gongsi/hangzhou_shangyezhongxin_o5"
]
file = open("wealink_gongsi_basic.txt","w")
for gurl in glist:
	url = gurl+"_s/"
	result = re.sub(' +', ' ', urllib2.urlopen(urllib2.Request(url, headers=headers)).read().replace("\n","").replace("\t","").replace("&nbsp;",""))
	total = int(re.findall('<b class="clr-org">(.*?)</b>', result)[0])
	for i in range(1,min(total/10+1,101)):
		url = gurl+"_p"+str(i)+"_s/"
		result = re.sub(' +', ' ', urllib2.urlopen(urllib2.Request(url, headers=headers)).read().replace("\n","").replace("\t","").replace("&nbsp;",""))
		links = [[item.split("/")[0], item.split("\"")[2]] for item in re.findall('<h4><a target="_blank" href="http://www.wealink.com/gongsi/shouye/(.*?)" class="fnt-14 clr-08c">', result)]
		basic = [re.sub('<.*?>', '', item).strip().replace(" ","") for item in re.findall('<p class="gssx">(.*?)</p>', result)]
		pnums = [re.sub('<.*?>', '', item).strip().replace(" ","") for item in re.findall('<p class="gsxg">(.*?)</p>', result)]
		print gurl, i, len(links), len(basic)
		for j in xrange(len(links)):
			file.write(links[j][0]+"\t"+links[j][1]+"\t"+basic[j]+"\t"+pnums[j]+"\n")
file.close()

file = open("wealink_gongsi_info.txt","w")
for line in fileinput.input("wealink_gongsi_basic.txt"):
	try:
		gid = line.split("\t")[0]
		url = "http://www.wealink.com/gongsi/shouye/"+gid
		result = re.sub(' +', ' ', urllib2.urlopen(urllib2.Request(url, headers=headers)).read().replace("\n","").replace("\t","").replace("&nbsp;",""))
		addr = re.findall('<span title="(.*?)">', result)[0].replace("&","").replace("#","").replace(" ","").split(";")[0]
		print gid, "http://api.map.baidu.com/geocoder?address="+addr+"&output=json&key=hIlimGuvEfHV41Aw885gONzB&city=杭州"
		res = json.loads(urllib2.urlopen(urllib2.Request("http://api.map.baidu.com/geocoder?address="+addr+"&output=json&key=hIlimGuvEfHV41Aw885gONzB&city=杭州")).read())
		avg, low, high = re.findall('<td class="average clr-org">(.*?)</td>', result)[0] if len(re.findall('<td class="average clr-org">(.*?)</td>', result))>=1 else "0", re.findall('<span class="low clr-org">(.*?)</span></td>', result)[0] if len(re.findall('<span class="low clr-org">(.*?)</span></td>', result))>=1 else "0", re.findall('<span class="flag clr-org">(.*?)</span></td>', result)[0] if len(re.findall('<span class="flag clr-org">(.*?)</span></td>', result))>=1 else "0"
		print res.has_key("result")
		poi = str(res["result"]["location"]["lng"])+","+str(res["result"]["location"]["lat"]) if addr!="浙江-杭州" and res.has_key("result") and len(res["result"])==4 else "None"
		file.write(gid+"\t"+addr+"\t"+poi+"\t"+avg+"\t"+low+"\t"+high+"\n")
	except:
		continue
file.close()

file = open("ganji_yiyuan.txt","w")
for p in range(1,300):
	print p
	url = "http://hz.yiliao.ganji.com/zhaoyiyuan/p"+str(p)+"/"
	print url
	result = urllib2.urlopen(urllib2.Request(url, headers=headers)).read().replace("\r\n","").replace("&nbsp;","")
	basics = re.findall('<div class="clearfix"><a target="_blank" href="http://hz.yiliao.ganji.com/yiyuan/(.*?)</a></div>', result)
	infos = re.findall('<span class="left_width1">(.*?)</div>', result)
	for i in xrange(len(basics)):
		yid, name, info = basics[i].split(".")[0], basics[i].split(">")[-1], re.sub(' +', ' ', re.sub('<.*?>', '', infos[::2][i]))
		file.write(yid+"\t"+name+"\t"+info+"\n")
	time.sleep(random.uniform(0, 3))
file.close()

file = open("ganji_yiyuan_info.txt","a")
i = 0
for line in fileinput.input("ganji_yiyuan.txt"):
	i+=1
	if i <= 1962:
		continue
	yid = line.split("\t")[0]
	url = "http://hz.yiliao.ganji.com/yiyuan/"+yid+".html"
	result = urllib2.urlopen(urllib2.Request(url, headers=headers)).read().replace("\r\n","").replace("&nbsp;","")
	addr = re.findall('<span class="dz">(.*?)</span>', result)[0]
	res = json.loads(urllib2.urlopen(urllib2.Request("http://api.map.baidu.com/geocoder?address="+addr+"&output=json&key=hIlimGuvEfHV41Aw885gONzB&city=杭州")).read())
	poi = str(res["result"]["location"]["lng"])+","+str(res["result"]["location"]["lat"]) if addr!="浙江-杭州" and res.has_key("result") and len(res["result"])==4 else "None"
	infos = re.sub(' +', ' ', re.sub('<.*?>', ' ', re.findall('<div class="tle"><h2 id="keshi">全部科室</h2></div>(.*?)</div>', result)[0])).strip() if len(re.findall('<div class="tle"><h2 id="keshi">全部科室</h2></div>(.*?)</div>', result)) == 1 else "None"
	print poi
	file.write(yid+"\t"+addr+"\t"+poi+"\t"+infos+"\n")
	time.sleep(random.uniform(0, 3))
file.close()

file = open("anjuke_sp_chushou.txt","w")
for p in xrange(99):
	print p
	url = "http://hz.sp.anjuke.com/shou/p"+str(p)+"/"
	result = urllib2.urlopen(urllib2.Request(url, headers=headers)).read().replace("\r\n","").replace("&nbsp;","")
	links = re.findall('<a class="t" data-sign="true" href="(.*?)"  target="_blank">', result)
	for link in links:
		file.write(link+"\n")
file.close()

file = open("anjuke_sp_chushou_info.txt","a")
i = 0
for link in fileinput.input("anjuke_sp_chushou.txt"):
	i+=1
	if i <= 2225:
		continue
	# try:
	url = link.strip()
	result = urllib2.urlopen(urllib2.Request(url, headers=headers)).read().replace("\r\n","").replace("&nbsp;","")
	# print result
	# price = re.sub('<.*?>', ' ', re.findall('class="prices">(.*?)</span>', result)[0]).replace(" ","").replace("&nbsp;","").replace("&bull;","")
	price = re.sub('<.*?>', ' ', re.findall('class="price">(.*?)</span>', result)[0]).replace(" ","").replace("&nbsp;","").replace("&bull;","")
	# price_sum = re.sub('<.*?>', ' ', re.findall('<span class="price_new_sma">(.*?)</span>', result)[0]).replace(" ","").replace("&nbsp;","").replace("&bull;","")
	# price_sum = re.sub('<.*?>', ' ', re.findall('<strong class="numbers numfont">(.*?)</span>', result)[0]).replace(" ","").replace("&nbsp;","").replace("&bull;","")
	# property_cost = re.sub('<.*?>', ' ', re.findall('<span class="font_st">(.*?)</span>', result)[0]).replace(" ","").replace("&nbsp;","").replace("&bull;","")
	area = re.sub('<.*?>', ' ', re.findall('建筑面积：(.*?)</li>', result)[0]).replace(" ","").replace("&nbsp;","")
	info = re.sub(' +', ' ', re.sub('<.*?>', ' ', re.findall('<ul class="office-datum1 clearboth">(.*?)</ul>', result)[1])).replace("&nbsp;","").strip()
	para = re.sub(' +', ' ', re.sub('<.*?>', ' ', re.findall('<table class="house-attr">(.*?)</table>', result)[0])).replace("&nbsp;","").replace("&gt;","").strip() if len(re.findall('<table class="house-attr">(.*?)</table>', result)) != 0 else "None"
	poi = re.findall('http://api.map.baidu.com/staticimage(.*?)zoom=', result)[0].split("=")[1].split("&")[0] if len(re.findall('http://api.map.baidu.com/staticimage(.*?)zoom=', result)) != 0 else "None" 
	if poi == "None":
		addr = re.sub('<.*?>', ' ', re.findall('<strong>地址：</strong>(.*?)<li>', result)[0]).replace(" ","").replace("&nbsp;","") if len(re.findall('<strong>地址：</strong>(.*?)<li>', result)) != 0 else re.sub('<.*?>', ' ', re.findall('<strong>位置：</strong>(.*?)<li>', result)[0]).replace(" ","").replace("&nbsp;","") if len(re.findall('<strong>位置：</strong>(.*?)<li>', result)) != 0 else "None"
		res = json.loads(urllib2.urlopen(urllib2.Request("http://api.map.baidu.com/geocoder?address="+addr+"&output=json&key=hIlimGuvEfHV41Aw885gONzB&city=杭州")).read())
		poi = str(res["result"]["location"]["lng"])+","+str(res["result"]["location"]["lat"]) if addr!="浙江-杭州" and res.has_key("result") and len(res["result"])==4 else "None"
	print url, poi
	file.write(url+"\t"+price+"\t"+area+"\t"+info+"\t"+para+"\t"+poi+"\n")
	# except:
	# 	continue
fileinput.close()
file.close()

file = open("anjuke_loupan_info.txt","w")
for p in range(1, 103):
	print p
	url = "http://hz.xzl.anjuke.com/loupan/p"+str(p)+"/"
	result = re.sub(' +', ' ', urllib2.urlopen(urllib2.Request(url, headers=headers)).read().replace("\n","")).replace("&nbsp;","")
	blocks = re.findall('<div class="bdl_mic_nrjj">(.*?)<div class="bdl_mic_ps">', result)
	for block in blocks:
		link = re.findall('<a target="_blank" href="(.*?)</a>', block)[0].split("\"")[0]
		name = re.sub('<.*?>', ' ', re.findall('<a target="_blank" href="(.*?)</a>', block)[0].split(">")[1]).strip()
		info = re.sub(' +', ' ', re.sub('<.*?>', ' ', re.findall('<p class="new_prop_title"></p>(.*?)<p class="bdl_options">', block)[0])).strip()
		price1 = re.sub(' +', ' ', re.sub('<.*?>', ' ', re.findall('<p>售价：(.*?)</p>', block)[0])).strip() if len(re.findall('<p>售价：(.*?)</p>', block)) == 1 else "None"
		price2 = re.sub(' +', ' ', re.sub('<.*?>', ' ', re.findall('<p>租金：(.*?)</p>', block)[0])).strip() if len(re.findall('<p>租金：(.*?)</p>', block)) == 1 else "None"
		result_inner = re.sub(' +', ' ', urllib2.urlopen(urllib2.Request(link, headers=headers)).read().replace("\n","")).replace("&nbsp;","")
		poi = re.findall('http://api.map.baidu.com/staticimage(.*?)zoom=', result_inner)[0].split("=")[1].split("&")[0] if len(re.findall('http://api.map.baidu.com/staticimage(.*?)zoom=', result_inner)) != 0 else "None" 
		if poi == "None":
			addr = re.sub('<.*?>', ' ', re.findall('<em>楼盘地址：&nbsp;</em><span class="l-info-val">(.*?)</span>', result)[0]).replace(" ","").replace("&nbsp;","") if len(re.findall('<strong>地址：</strong>(.*?)<li>', result)) != 0 else re.sub('<.*?>', ' ', re.findall('<strong>位置：</strong>(.*?)<li>', result)[0]).replace(" ","").replace("&nbsp;","") if len(re.findall('<strong>位置：</strong>(.*?)<li>', result)) != 0 else "None"
			res = json.loads(urllib2.urlopen(urllib2.Request("http://api.map.baidu.com/geocoder?address="+addr+"&output=json&key=hIlimGuvEfHV41Aw885gONzB&city=杭州")).read())
			poi = str(res["result"]["location"]["lng"])+","+str(res["result"]["location"]["lat"]) if addr!="浙江-杭州" and res.has_key("result") and len(res["result"])==4 else "None"
		file.write(link+"\t"+name+"\t"+info+"\t"+price1+"\t"+price2+"\t"+poi+"\n")
file.close()

file = open("sxue_info.txt","w")
for p in range(1, 60):
	print p
	url = "http://xuexiao.51sxue.com/slist/?searchKey=%BA%BC%D6%DD&page="+str(p)
	result = re.sub(' +', ' ', urllib2.urlopen(urllib2.Request(url, headers=headers)).read().decode('gb2312','ignore').encode("utf-8").replace("\r\n","")).replace("&nbsp;","")
	blocks = re.findall('<div class="school_m_main fl">(.*?)</ul>', result)
	for block in blocks:
		info = re.sub(' +', ' ', re.sub('<.*?>', ' ', re.findall('target="_blank" id="dsadas">(.*?)<div class="school_m_df fl">', block)[0]))
		pnum = re.sub(' +', ' ', re.sub('<.*?>', ' ', re.findall('<div class="school_m_text">已有<b>(.*?)</b>位网友对学校评分</div>', block)[0]))
		score = re.sub(' +', ' ', re.sub('<.*?>', ' ', re.findall('<div class="school_m_tu"><img src="http://img.51sxue.com/newtpl/images/(.*?).gif" align="middle"/></div>', block)[0]))
		addr = re.sub('<.*?>', ' ', re.findall('<li class="school_dz">学校地址:<b>(.*?)</b></li>', block)[0]).replace(" ","")
		res = json.loads(urllib2.urlopen(urllib2.Request("http://api.map.baidu.com/geocoder?address="+addr+"&output=json&key=hIlimGuvEfHV41Aw885gONzB&city=杭州")).read())
		poi = str(res["result"]["location"]["lng"])+","+str(res["result"]["location"]["lat"]) if addr!="浙江-杭州" and res.has_key("result") and len(res["result"])==4 else "None"
		file.write(info+"\t"+pnum+"\t"+score+"\t"+addr+"\t"+poi+"\n")
file.close()

list = [
["http://www.hzws.gov.cn/site/show.asp?id=31950","2013-11"],
["http://www.hzws.gov.cn/site/show.asp?id=32092","2013-12"],
["http://www.hzws.gov.cn/site/show.asp?id=32489","2014-01"],
["http://www.hzws.gov.cn/site/show.asp?id=32664","2014-02"],
["http://www.hzws.gov.cn/site/show.asp?id=32667","2014-03"],
["http://www.hzws.gov.cn/site/show.asp?id=32927","2014-04"],
["http://www.hzws.gov.cn/site/show.asp?id=33127","2014-05"],
["http://www.hzws.gov.cn/site/show.asp?id=33355","2014-06"],
["http://www.hzws.gov.cn/site/show.asp?id=33677","2014-07"],
["http://www.hzws.gov.cn/site/show.asp?id=33746","2014-08"],
["http://www.hzws.gov.cn/site/show.asp?id=34033","2014-09"],
]
file = open("hzgov_yiyuan.txt","a")
p = 10
url = list[p][0]
result = urllib2.urlopen(urllib2.Request(url, headers=headers)).read().decode('gb2312','ignore').encode("utf-8").replace("\n","").replace("&nbsp;","")
# blocks = re.findall('<TD style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #ece9d8; PADDING-BOTTOM: 0cm; BACKGROUND-COLOR: transparent; PADDING-LEFT: 5.4pt; WIDTH: 102pt;(.*?)</TR>', result)
# blocks = re.findall('<TD style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #ece9d8; PADDING-BOTTOM: 0cm; BACKGROUND-COLOR: transparent; PADDING-LEFT: 5.4pt; WIDTH: 107.75pt(.*?)</TR>', result)
# blocks = re.findall('<TD style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #ece9d8; PADDING-BOTTOM: 0cm; BACKGROUND-COLOR: transparent; PADDING-LEFT: 5.4pt; WIDTH: 85.75pt;(.*?)</TR>', result)
# blocks = re.findall('<TD style="BORDER-BOTTOM: windowtext 0.5pt solid; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 143pt;(.*?)</TR>', result)
# blocks = re.findall('<TD style="BORDER-BOTTOM: windowtext 0.5pt solid; BORDER-LEFT: windowtext; BACKGROUND-COLOR: transparent; WIDTH: 143pt;(.*?)</TR>', result)
# blocks = re.findall('<TD style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #ece9d8; PADDING-BOTTOM: 0cm; BACKGROUND-COLOR: transparent; PADDING-LEFT: 5.4pt; WIDTH: 122.75pt;(.*?)</TR>', result)
# blocks = re.findall('<TD style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #ece9d8; PADDING-BOTTOM: 0cm; BACKGROUND-COLOR: transparent; PADDING-LEFT: 5.4pt; WIDTH: 112.25pt;(.*?)</TR>', result)
# blocks = re.findall('<TD style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0cm; BACKGROUND-COLOR: transparent; PADDING-LEFT: 5.4pt; WIDTH: 134pt;(.*?)</TR>', result)
# blocks = re.findall('<TD style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0cm; BACKGROUND-COLOR: transparent; PADDING-LEFT: 5.4pt; WIDTH: 134pt;(.*?)</TR>', result)
# blocks = re.findall('<TD style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0cm; BACKGROUND-COLOR: transparent; PADDING-LEFT: 5.4pt; WIDTH: 134pt;(.*?)</TR>', result)
blocks = re.findall('<TD style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: #f0f0f0; PADDING-BOTTOM: 0cm; BACKGROUND-COLOR: transparent; PADDING-LEFT: 5.4pt; WIDTH: 134pt;(.*?)</TR>', result)
print list[p][1], len(blocks)
for block in blocks[1:]:
	# print re.sub(' +', ' ', re.sub('<.*?>', ' ', block)).split(">")[1].strip()
	file.write(list[p][1]+"\t"+re.sub(' +', ' ', re.sub('<.*?>', ' ', block)).split(">")[1].strip()+"\n")
file.close()

list = [
["http://www.hzws.gov.cn/site/show.asp?id=32094","2013-4J"],
["http://www.hzws.gov.cn/site/show.asp?id=32841","2014-1J"],
["http://www.hzws.gov.cn/site/show.asp?id=33414","2014-2J"],
["http://www.hzws.gov.cn/site/show.asp?id=34068","2014-3J"],
]
file = open("hzgov_yiyuan_J.txt","a")
p = 3
url = list[p][0]
result = urllib2.urlopen(urllib2.Request(url, headers=headers)).read().decode('gb2312','ignore').encode("utf-8").replace("\n","").replace("&nbsp;","")
# blocks = re.findall('<TD style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext 1pt solid; PADDING-BOTTOM: 0cm; BACKGROUND-COLOR: transparent; PADDING-LEFT: 5.4pt; WIDTH: 81.75pt;(.*?)</TR>', result)
# blocks = re.findall('<TR style="HEIGHT: 40.5pt; mso-height-source: userset" height=54>(.*?)</TR>', result)
# blocks = re.findall('<TD style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext 1pt solid; PADDING-BOTTOM: 0cm; BACKGROUND-COLOR: transparent; PADDING-LEFT: 5.4pt; WIDTH: 101pt;(.*?)</TR>', result)
blocks = re.findall('<TD style="BORDER-BOTTOM: windowtext 1pt solid; BORDER-LEFT: windowtext 1pt solid; PADDING-BOTTOM: 0cm; BACKGROUND-COLOR: transparent; PADDING-LEFT: 5.4pt; WIDTH: 64.55pt;(.*?)</TR>', result)
print list[p][1], len(blocks)
for block in blocks[1:]:
	# print re.sub(' +', ' ', re.sub('<.*?>', ' ', block)).split(">")[1].strip()
	file.write(list[p][1]+"\t"+re.sub(' +', ' ', re.sub('<.*?>', ' ', block)).split(">")[1].strip()+"\n")
file.close()

file = open("hzgov_zytj.txt","a")
for p in range(1, 43):
	print p
	p = "" if p == 1 else p
	url = "http://www.hzgtj.gov.cn:81/jpm/static/ztbj/tdsc/cjxx/P-1031168b49b-10021"+str(p)+".html"
	result = urllib2.urlopen(urllib2.Request(url, headers=headers)).read().replace("\r\n","").replace("&nbsp;","")
	blocks = re.findall('<tr >(.*?)</tr>', result)
	for block in blocks[1:]:
		info = re.sub(' +', ' ', re.sub('<.*?>', ' ', re.sub('<script(.*?)</script>', ' ', block))).strip()
		tm = re.findall('var sinfodate=\'(.*?) 00:00:00.0\'', block)[0]
		addr = info.split(" ")[1]
		res = json.loads(urllib2.urlopen(urllib2.Request("http://api.map.baidu.com/geocoder?address="+addr+"&output=json&key=hIlimGuvEfHV41Aw885gONzB&city=杭州")).read())
		poi = str(res["result"]["location"]["lng"])+","+str(res["result"]["location"]["lat"]) if addr!="浙江-杭州" and res.has_key("result") and len(res["result"])==4 else "None"
		file.write(info+"\t"+tm+"\t"+poi+"\n")
		print tm, addr, poi
file.close()

file = open("hzjtydzs.txt","a")
while True:
	try:
		url = "http://www.hzjtydzs.com/web/xmlsvc/currentRoadSpeed.aspx?rank=细粒度&order=asc&areaid="
		result, now = urllib2.urlopen(urllib2.Request(url, headers=headers), timeout=30).read(), ""
		for line in result.split("\n"):
			if "serverTime" in line:
				now = line.split("\"")[1]
			if "roadName" in line:
				file.write(now+"\t"+" ".join(line.split("\"")[1::2])+"\n")
		time.sleep(60)
	except:
		continue
file.close()

url = "http://www.hzjtydzs.com/web/xmlsvc/currentRoadSpeed.aspx?rank=细粒度&order=asc&areaid="
result = urllib2.urlopen(urllib2.Request(url, headers=headers), timeout=30).read()
for line in result.split("\n"):
	if "roadName" in line:
		addr = line.split("\"")[1].replace(" ","")
		res = json.loads(urllib2.urlopen(urllib2.Request("http://api.map.baidu.com/geocoder?address="+addr+"&output=json&key=hIlimGuvEfHV41Aw885gONzB&city=杭州")).read())
		poi = str(res["result"]["location"]["lng"])+","+str(res["result"]["location"]["lat"]) if addr!="浙江-杭州" and res.has_key("result") and len(res["result"])==4 else "None"
		print addr, poi

file = open("epmap_AQI.txt","w")
for filename in sorted(glob.glob(r"AQI/浙江省_*.csv")):
	for line in fileinput.input(filename):
		if "杭州" in line:
			file.write(line)
file.close()

headers = {'Connection':'keep-alive',
'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
'Cookie':'JSESSIONID=DA2F6C615C8FD0D18B3A67CE159B580D'}
# headers['Referer'] = "http://218.108.6.116:8080/zxjc/datashow_getdatashowhtml?wrlx=1&xzqy=0&sjlx=hour&kssj=2014-11-01,00"
file = open("zxjc.txt","w")
for m in range(4,12):
	for d in range(1,32):
		for h in xrange(0,24):
			tm = "2014"+"-"+str(m).zfill(2)+"-"+str(d).zfill(2)+","+str(h).zfill(2)
			url = "http://218.108.6.116:8080/zxjc/datashow_getdatashowhtml?wrlx=1&xzqy=0&sjlx=hour&kssj="+tm
			result = urllib2.urlopen(urllib2.Request(url, headers=headers)).read().decode('gb2312','ignore').encode("utf-8").replace("&nbsp;","")
			blocks = re.findall('<td class="checkBoxs"(.*?)</tr>', result)
			for block in blocks:
				file.write(tm+"\t"+re.sub(' +', ' ', re.sub('^.*?>', ' ', re.sub('<.*?>', ' ', block))).strip()+"\n")
				print "1", tm, re.sub(' +', ' ', re.sub('^.*?>', ' ', re.sub('<.*?>', ' ', block))).strip()
			for p in range(2,14):
				url = "http://218.108.6.116:8080/zxjc/datashow_page?destiny_page="+str(p)
				print url
				result = urllib2.urlopen(urllib2.Request(url, headers=headers)).read().decode('gb2312','ignore').encode("utf-8").replace("&nbsp;","")
				blocks = re.findall('<td class="checkBoxs"(.*?)</tr>', result)
				for block in blocks:
					file.write(tm+"\t"+re.sub(' +', ' ', re.sub('^.*?>', ' ', re.sub('<.*?>', ' ', block))).strip()+"\n")
					print p, tm, re.sub(' +', ' ', re.sub('^.*?>', ' ', re.sub('<.*?>', ' ', block))).strip()
file.close()

file = open("school_info_7.txt","w")
for line in fileinput.input("school_info/school_info_7.txt"):
	file.write("\t".join(line.strip().split("\t")[0:17])+"\n")
fileinput.close()
file.close()

file = open("dianping_info.txt","w")
areas = ["58","59","60","61","62","63","6446","8864"]
for line in fileinput.input("dianping_urls.txt"):
	for area in areas:
		try:
			url = line.strip()+"o2r"+area
			print url
			result = urllib2.urlopen(urllib2.Request(url, headers=headers)).read().replace("\n","")
			tp = int(re.findall('<span class="num">(.*?)</span>', result)[0].replace("(","").replace(")",""))
			for p in range(1,min(tp/15+2,51)):
				url = line.strip()+"o2r"+area+"p"+str(p)
				result = urllib2.urlopen(urllib2.Request(url, headers=headers)).read().replace("\n","")
				blocks = re.findall('<div class="txt">(.*?)<div class="operate J_operate Hide">', result)
				print url, len(blocks)
				for block in blocks:
					link = "http://www.dianping.com/shop/"+re.findall('href="/shop/(.*?)"', block)[0]
					file.write(url+"\t"+link+"\t"+re.sub(' +', ' ', re.sub('<.*?>', ' ', block)).strip()+"\n")
		except:
			continue
fileinput.close()
file.close()

file = open("dianping_info_poi.txt","w")
for line in fileinput.input("dianping_info_1.txt"):
	url = line.split("\t")[1]
	print url
	result = urllib2.urlopen(urllib2.Request(url, headers=headers)).read().replace("\n","")
	poi = re.findall('\({lng:(.*?)}\);', result)[0].replace("lat:","") if len(re.findall('\({lng:(.*?)}\);', result)) != 0 else "None"
	if poi == "None":
		addr = "杭州市"+re.sub('<.*?>', ' ', re.findall('<span itemprop="locality region">(.*?)</div>', result)[0]).replace(" ","") if len(re.findall('<span itemprop="locality region">(.*?)</div>', result)) != 0 else "None"
		res = json.loads(urllib2.urlopen(urllib2.Request("http://api.map.baidu.com/geocoder?address="+addr+"&output=json&key=hIlimGuvEfHV41Aw885gONzB&city=杭州")).read())
		poi = str(res["result"]["location"]["lng"])+","+str(res["result"]["location"]["lat"]) if addr!="浙江-杭州" and res.has_key("result") and len(res["result"])==4 else "None"
	file.write(poi+"\t"+line)
fileinput.close()
file.close()

file = open("tutiempo.txt","w")
for p in range(4,12):
	print p
	url = "http://www.tutiempo.net/en/Climate/Hangzhou/"+str(p).zfill(2)+"-2014/584570.htm"
	result = urllib2.urlopen(urllib2.Request(url, headers=headers)).read()
	blocks = re.findall('<td><strong>(.*?)</td></tr><tr>', result)
	for block in blocks:
		file.write("2014"+"\t"+str(p).zfill(2)+"\t"+re.sub('<.*?>', ' ', block.replace("</td><td>","\t")).replace("&nbsp;","")+"\n")
file.close()		
