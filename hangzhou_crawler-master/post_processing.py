# -*- coding: utf-8 -*-

import re
import json
import urllib
import urllib2
import fileinput

file = open("data/dianping/dianping_info_poi_1.txt","w")
for line in fileinput.input("organized/dianping/dianping_info_poi_1.txt"):
	try:
		poi = line.strip().split("\t")[0]
		tp = "/".join(line.strip().split("\t")[1].split("o")[-2].split("/")[-3:])
		name = line.strip().split("\t")[3].split("|")[0].split(" ")[0]
		price = line.strip().split("\t")[3].split("|")[1].split(" ")[2]
		count = re.findall('([0-9]*?) 条点评', line.strip().split("\t")[3].split("|")[0])[0] if len(re.findall('([0-9]*?) 条点评', line.strip().split("\t")[3].split("|")[0]))!=0 else "0"
		score = "\t".join(re.findall('([0-9]\.[0-9])', line.strip().split("\t")[3].split("|")[2])) if len(re.findall('([0-9]\.[0-9])', line.strip().split("\t")[3].split("|")[2]))!=0 else "-\t-\t-"
		file.write(poi+"\t"+name+"\t"+tp+"\t"+price+"\t"+count+"\t"+score+"\n")
	except:
		continue
fileinput.close()
file.close()

file = open("data/fangchan/anjuke_loupan_info.txt","w")
for line in fileinput.input("organized/fangchan/anjuke_loupan_info.txt"):
	part = line.strip().split("\t")
	s1 = re.findall('类型：(.*?) ', part[2])[0] if len(re.findall('类型：(.*?) ', part[2]))!=0 else "None"
	s2 = re.findall('总楼层：(.*?)层 ', part[2])[0] if len(re.findall('总楼层：(.*?)层 ', part[2]))!=0 else "None"
	s3 = re.findall('物业费：(.*?)元/平米•月 ', part[2])[0] if len(re.findall('物业费：(.*?)元/平米•月 ', part[2]))!=0 else "None"
	s4 = re.findall('竣工年月：(.*?)$', part[2])[0] if len(re.findall('竣工年月：(.*?)$', part[2]))!=0 else "None"
	s5 = re.findall('(.*?) 元/平米', part[3])[0] if len(re.findall('(.*?) 元/平米', part[3]))!=0 else "None"
	s6 = re.findall('(.*?) 元/平米•天', part[4])[0] if len(re.findall('(.*?) 元/平米•天', part[4]))!=0 else "None"
	file.write(part[5]+"\t"+s1+"\t"+s2+"\t"+s3+"\t"+s4+"\t"+s5+"\t"+s6+"\n")
fileinput.close()
file.close()

file = open("data/fangchan/anjuke_sp_chushou_info.txt","w")
for line in fileinput.input("organized/fangchan/anjuke_sp_chushou_info.txt"):
	part = line.strip().split("\t")
	s1 = re.findall('(.*?)万元', part[1])[0] if len(re.findall('(.*?)万元', part[1]))!=0 else "None"
	s2 = re.findall('(.*?)平米', part[2])[0] if len(re.findall('(.*?)平米', part[2]))!=0 else "None"
	s3 = re.findall('物业： (.*?) ', part[3])[0] if len(re.findall('物业： (.*?) ', part[3]))!=0 else "None"
	s4 = re.findall('类型： (.*?) ', part[3])[0] if len(re.findall('类型： (.*?) ', part[3]))!=0 else "None"
	s5 = re.findall('楼层： (.*?)层 ', part[3])[0] if len(re.findall('楼层： (.*?)层 ', part[3]))!=0 else "None"
	s6 = re.findall('状态： (.*?)$', part[3])[0] if len(re.findall('状态： (.*?)$', part[3]))!=0 else "None"
	s7 = re.findall('开发商： (.*?) ', part[4])[0] if len(re.findall('开发商： (.*?) ', part[4]))!=0 and re.findall('开发商： (.*?) ', part[4])[0].strip()!="" and "：" not in re.findall('开发商： (.*?) ', part[4])[0].strip() else "None"
	s8 = re.findall('竣工时间： (.*?) ', part[4])[0] if len(re.findall('竣工时间： (.*?) ', part[4]))!=0 and re.findall('竣工时间： (.*?) ', part[4])[0].strip()!="" and "：" not in re.findall('竣工时间： (.*?) ', part[4])[0].strip() else "None"
	s9 = re.findall('是否统一管理： (.*?) ', part[4])[0] if len(re.findall('是否统一管理： (.*?) ', part[4]))!=0 and re.findall('是否统一管理： (.*?) ', part[4])[0].strip()!="" and "：" not in re.findall('是否统一管理： (.*?) ', part[4])[0].strip() else "None"
	s10 = re.findall('物业公司： (.*?) ', part[4])[0] if len(re.findall('物业公司： (.*?) ', part[4]))!=0 and re.findall('物业公司： (.*?) ', part[4])[0].strip()!="" and "：" not in re.findall('物业公司： (.*?) ', part[4])[0].strip() else "None"
	s11 = re.findall('总楼层： (.*?)层', part[4])[0] if len(re.findall('总楼层： (.*?)层', part[4]))!=0 and re.findall('总楼层： (.*?)层', part[4])[0].strip()!="" else "None"
	s12 = re.findall('物业费： (.*?)元/平米•月', part[4])[0] if len(re.findall('物业费： (.*?)元/平米•月', part[4]))!=0 and re.findall('物业费： (.*?)元/平米•月', part[4])[0].strip()!="" else "None"
	s13 = re.findall('总面积： (.*?)平米', part[4])[0] if len(re.findall('总面积： (.*?)平米', part[4]))!=0 and re.findall('总面积： (.*?)平米', part[4])[0].strip()!="" else "None"
	file.write(part[5]+"\t"+s1+"\t"+s2+"\t"+s3+"\t"+s4+"\t"+s5+"\t"+s6+"\t"+s7+"\t"+s8+"\t"+s9+"\t"+s10+"\t"+s11+"\t"+s12+"\t"+s13+"\n")
fileinput.close()
file.close()

file = open("data/fangchan/anjuke_sp_chuzu_info.txt","w")
for line in fileinput.input("organized/fangchan/anjuke_sp_chuzu_info.txt"):
	part = line.strip().split("\t")
	s1 = re.findall('(.*?)元/月', part[1])[0] if len(re.findall('(.*?)元/月', part[1]))!=0 else "None"
	s2 = re.findall('(.*?)元/平米', part[2])[0] if len(re.findall('(.*?)元/平米', part[2]))!=0 else "None"
	s3 = re.findall('(.*?)平米', part[3])[0] if len(re.findall('(.*?)平米', part[3]))!=0 else "None"
	s4 = re.findall('物业： (.*?) ', part[4])[0] if len(re.findall('物业： (.*?) ', part[4]))!=0 else "None"
	s5 = re.findall('类型： (.*?) ', part[4])[0] if len(re.findall('类型： (.*?) ', part[4]))!=0 else "None"
	s6 = re.findall('楼层： (.*?)层 ', part[4])[0] if len(re.findall('楼层： (.*?)层 ', part[4]))!=0 else "None"
	s7 = re.findall('状态： (.*?)$', part[4])[0] if len(re.findall('状态： (.*?)$', part[4]))!=0 else "None"
	s8 = re.findall('开发商： (.*?) ', part[5])[0] if len(re.findall('开发商： (.*?) ', part[5]))!=0 and re.findall('开发商： (.*?) ', part[5])[0].strip()!="" and "：" not in re.findall('开发商： (.*?) ', part[5])[0].strip() else "None"
	s9 = re.findall('竣工时间： (.*?) ', part[5])[0] if len(re.findall('竣工时间： (.*?) ', part[5]))!=0 and re.findall('竣工时间： (.*?) ', part[5])[0].strip()!="" and "：" not in re.findall('竣工时间： (.*?) ', part[5])[0].strip() else "None"
	s10 = re.findall('是否统一管理： (.*?) ', part[5])[0] if len(re.findall('是否统一管理： (.*?) ', part[5]))!=0 and re.findall('是否统一管理： (.*?) ', part[5])[0].strip()!="" and "：" not in re.findall('是否统一管理： (.*?) ', part[5])[0].strip() else "None"
	s11 = re.findall('物业公司： (.*?) ', part[5])[0] if len(re.findall('物业公司： (.*?) ', part[5]))!=0 and re.findall('物业公司： (.*?) ', part[5])[0].strip()!="" and "：" not in re.findall('物业公司： (.*?) ', part[5])[0].strip() else "None"
	s12 = re.findall('总楼层： (.*?)层', part[5])[0] if len(re.findall('总楼层： (.*?)层', part[5]))!=0 and re.findall('总楼层： (.*?)层', part[5])[0].strip()!="" else "None"
	s13 = re.findall('物业费： (.*?)元/平米•月', part[5])[0] if len(re.findall('物业费： (.*?)元/平米•月', part[5]))!=0 and re.findall('物业费： (.*?)元/平米•月', part[5])[0].strip()!="" else "None"
	s14 = re.findall('总面积： (.*?)平米', part[5])[0] if len(re.findall('总面积： (.*?)平米', part[5]))!=0 and re.findall('总面积： (.*?)平米', part[5])[0].strip()!="" else "None"
	file.write(part[6]+"\t"+s1+"\t"+s2+"\t"+s3+"\t"+s4+"\t"+s5+"\t"+s6+"\t"+s7+"\t"+s8+"\t"+s9+"\t"+s10+"\t"+s11+"\t"+s12+"\t"+s13+"\t"+s14+"\n")
fileinput.close()
file.close()

file = open("data/fangchan/anjuke_xzl_chushou_info.txt","w")
for line in fileinput.input("organized/fangchan/anjuke_xzl_chushou_info.txt"):
	part = line.strip().split("\t")
	s1 = re.findall('(.*?)万元', part[1])[0] if len(re.findall('(.*?)万元', part[1]))!=0 else "None"
	s2 = re.findall('(.*?)元/平米', part[2])[0] if len(re.findall('(.*?)元/平米', part[2]))!=0 else "None"
	s3 = re.findall('(.*?)元/平米月', part[3])[0] if len(re.findall('(.*?)元/平米月', part[3]))!=0 else "None"
	s4 = re.findall('(.*?)平米', part[4])[0] if len(re.findall('(.*?)平米', part[4]))!=0 else "None"
	s5 = re.findall('楼盘： (.*?) ', part[5])[0] if len(re.findall('楼盘： (.*?) ', part[5]))!=0 else "None"
	s6 = re.findall('楼层： (.*?) ', part[5])[0] if len(re.findall('楼层： (.*?) ', part[5]))!=0 else "None"
	s7 = re.findall('类型： (.*?) ', part[5])[0] if len(re.findall('类型： (.*?) ', part[5]))!=0 else "None"
	s8 = re.findall('竣工： (.*?)$', part[5])[0] if len(re.findall('竣工： (.*?)$', part[5]))!=0 else "None"
	s9 = re.findall('竣工年月： (.*?) ', part[6])[0] if len(re.findall('竣工年月： (.*?) ', part[6]))!=0 and re.findall('竣工年月： (.*?) ', part[6])[0].strip()!="" else "None"
	s10 = re.findall('标准层面积： (.*?) ', part[6])[0] if len(re.findall('标准层面积： (.*?) ', part[6]))!=0 and re.findall('标准层面积： (.*?) ', part[6])[0].strip()!="" else "None"
	s11 = re.findall('总楼层： (.*?) ', part[6])[0] if len(re.findall('总楼层： (.*?) ', part[6]))!=0 and re.findall('总楼层： (.*?) ', part[6])[0].strip()!="" else "None"
	s12 = re.findall('物业公司： (.*?) ', part[6])[0] if len(re.findall('物业公司： (.*?) ', part[6]))!=0 and re.findall('物业公司： (.*?) ', part[6])[0].strip()!="" else "None"
	s13 = re.findall('空调类型： (.*?) ', part[6])[0] if len(re.findall('空调类型： (.*?) ', part[6]))!=0 and re.findall('空调类型： (.*?) ', part[6])[0].strip()!="" else "None"
	s14 = re.findall('大堂层高： (.*?) ', part[6])[0] if len(re.findall('大堂层高： (.*?) ', part[6]))!=0 and re.findall('大堂层高： (.*?) ', part[6])[0].strip()!="" else "None"
	s15 = re.findall('使用率： (.*?) ', part[6])[0] if len(re.findall('使用率： (.*?) ', part[6]))!=0 and re.findall('使用率： (.*?) ', part[6])[0].strip()!="" else "None"
	s16 = re.findall('电梯： (.*?) ', part[6])[0] if len(re.findall('电梯： (.*?) ', part[6]))!=0 and re.findall('电梯： (.*?) ', part[6])[0].strip()!="" else "None"
	s17 = re.findall('标准层高： (.*?) ', part[6])[0] if len(re.findall('标准层高： (.*?) ', part[6]))!=0 and re.findall('标准层高： (.*?) ', part[6])[0].strip()!="" else "None"
	s18 = re.findall('是否涉外： (.*?) ', part[6])[0] if len(re.findall('是否涉外： (.*?) ', part[6]))!=0 and re.findall('是否涉外： (.*?) ', part[6])[0].strip()!="" else "None"
	s19 = re.findall('车位： (.*?) ', part[6])[0] if len(re.findall('车位： (.*?) ', part[6]))!=0 and re.findall('车位： (.*?) ', part[6])[0].strip()!="" else "None"
	file.write(part[7]+"\t"+s1+"\t"+s2+"\t"+s3+"\t"+s4+"\t"+s5+"\t"+s6+"\t"+s7+"\t"+s8+"\t"+s9+"\t"+s10+"\t"+s11+"\t"+s12+"\t"+s13+"\t"+s14+"\t"+s15+"\t"+s16+"\t"+s17+"\t"+s18+"\t"+s19+"\n")
fileinput.close()
file.close()

file = open("data/fangchan/anjuke_xzl_zhaozu_info.txt","w")
for line in fileinput.input("organized/fangchan/anjuke_xzl_zhaozu_info.txt"):
	part = line.strip().split("\t")
	s1 = re.findall('(.*?)元/平米天', part[1])[0] if len(re.findall('(.*?)元/平米天', part[1]))!=0 else "None"
	s2 = re.findall('(.*?)元/月', part[2])[0] if len(re.findall('(.*?)元/月', part[2]))!=0 else "None"
	s3 = re.findall('(.*?)元/平米月', part[3])[0] if len(re.findall('(.*?)元/平米月', part[3]))!=0 else "None"
	s4 = re.findall('(.*?)平米', part[4])[0] if len(re.findall('(.*?)平米', part[4]))!=0 else "None"
	s5 = re.findall('楼盘： (.*?) ', part[5])[0] if len(re.findall('楼盘： (.*?) ', part[5]))!=0 else "None"
	s6 = re.findall('楼层： (.*?) ', part[5])[0] if len(re.findall('楼层： (.*?) ', part[5]))!=0 else "None"
	s7 = re.findall('类型： (.*?) ', part[5])[0] if len(re.findall('类型： (.*?) ', part[5]))!=0 else "None"
	s8 = re.findall('竣工： (.*?)$', part[5])[0] if len(re.findall('竣工： (.*?)$', part[5]))!=0 else "None"
	s9 = re.findall('竣工年月： (.*?) ', part[6])[0] if len(re.findall('竣工年月： (.*?) ', part[6]))!=0 and re.findall('竣工年月： (.*?) ', part[6])[0].strip()!="" else "None"
	s10 = re.findall('标准层面积： (.*?) ', part[6])[0] if len(re.findall('标准层面积： (.*?) ', part[6]))!=0 and re.findall('标准层面积： (.*?) ', part[6])[0].strip()!="" else "None"
	s11 = re.findall('总楼层： (.*?) ', part[6])[0] if len(re.findall('总楼层： (.*?) ', part[6]))!=0 and re.findall('总楼层： (.*?) ', part[6])[0].strip()!="" else "None"
	s12 = re.findall('物业公司： (.*?) ', part[6])[0] if len(re.findall('物业公司： (.*?) ', part[6]))!=0 and re.findall('物业公司： (.*?) ', part[6])[0].strip()!="" else "None"
	s13 = re.findall('空调类型： (.*?) ', part[6])[0] if len(re.findall('空调类型： (.*?) ', part[6]))!=0 and re.findall('空调类型： (.*?) ', part[6])[0].strip()!="" else "None"
	s14 = re.findall('大堂层高： (.*?) ', part[6])[0] if len(re.findall('大堂层高： (.*?) ', part[6]))!=0 and re.findall('大堂层高： (.*?) ', part[6])[0].strip()!="" else "None"
	s15 = re.findall('使用率： (.*?) ', part[6])[0] if len(re.findall('使用率： (.*?) ', part[6]))!=0 and re.findall('使用率： (.*?) ', part[6])[0].strip()!="" else "None"
	s16 = re.findall('电梯： (.*?) ', part[6])[0] if len(re.findall('电梯： (.*?) ', part[6]))!=0 and re.findall('电梯： (.*?) ', part[6])[0].strip()!="" else "None"
	s17 = re.findall('标准层高： (.*?) ', part[6])[0] if len(re.findall('标准层高： (.*?) ', part[6]))!=0 and re.findall('标准层高： (.*?) ', part[6])[0].strip()!="" else "None"
	s18 = re.findall('是否涉外： (.*?) ', part[6])[0] if len(re.findall('是否涉外： (.*?) ', part[6]))!=0 and re.findall('是否涉外： (.*?) ', part[6])[0].strip()!="" else "None"
	s19 = re.findall('车位： (.*?) ', part[6])[0] if len(re.findall('车位： (.*?) ', part[6]))!=0 and re.findall('车位： (.*?) ', part[6])[0].strip()!="" else "None"
	file.write(part[7]+"\t"+s1+"\t"+s2+"\t"+s3+"\t"+s4+"\t"+s5+"\t"+s6+"\t"+s7+"\t"+s8+"\t"+s9+"\t"+s10+"\t"+s11+"\t"+s12+"\t"+s13+"\t"+s14+"\t"+s15+"\t"+s16+"\t"+s17+"\t"+s18+"\t"+s19+"\n")
fileinput.close()
file.close()

file = open("data/gongjiao/lineshape.txt","w")
for line in fileinput.input("organized/gongjiao/lineshape.txt"):
	file.write(line.strip().split(";")[0]+"\t"+",".join(filter(lambda x:x.strip()!="", line.strip().split(";")[2].split(",")))+"\n")
fileinput.close()
file.close()

file = open("data/gongjiao/lineshape-baidu.txt","w")
c = 0
name, stops, dots = "", "", ""
for line in fileinput.input("organized/gongjiao/lineshape-baidu.txt"):
	if c%3 == 0:
		if name != "":
			file.write(name+"\t"+stops+"\t"+dots+"\n")
		name = line.strip()
	if c%3 == 1:
		stops = line.strip()
	if c%3 == 2:
		dots = line.strip()
	c = c+1
fileinput.close()
file.close()

file = open("data/gongsi/wealink_gongsi.txt","w")
map = {}
for line in fileinput.input("organized/gongsi/wealink_gongsi_basic.txt"):
	part = line.strip().split("\t")
	gid, info = part[0], part[1]+"\t"+"\t".join(part[2].split("|"))+"\t"+"\t".join(part[3].split("|"))
	map[gid] = info
fileinput.close()
for line in fileinput.input("organized/gongsi/wealink_gongsi_info.txt"):
	part = line.strip().split("\t")
	gid, poi, info = part[0], part[2]+"\t"+part[1], "\t".join(part[3:])
	file.write(poi+"\t"+map[gid]+"\t"+info+"\n")
fileinput.close()
file.close()

poimap = {
"滨江":"120.210,30.210",
"西溪":"120.063,30.274",
"云栖":"120.088,30.180",
"下沙":"120.348,30.305",
"卧龙桥":"120.128,30.246",
"临平镇":"120.300,30.418",
"城厢镇":"120.269,30.181",
"浙江农大":"120.193,30.268",
"朝晖五区":"120.167,30.292",
"和睦小学":"120.119,30.311"
}
file = open("data/huanjing/epmap_AQI.txt","w")
for line in fileinput.input("organized/huanjing/epmap_AQI.txt"):
	part = line.strip().split(",")
	tm, poi, info = part[0], part[3], "\t".join([i if i!="" else "-" for i in part[3:]])
	if poimap.has_key(poi):
		file.write(tm+"\t"+poimap[poi]+"\t"+info+"\n")
fileinput.close()
file.close()

### step A ####
map = {}
for line in fileinput.input("organized/huanjing/zxjc_1.txt"):
	map[re.sub('\（.*?\）', '', re.sub('\(.*?\)', '', line.strip().split(" ")[0]))] = True
fileinput.close()
for line in fileinput.input("organized/huanjing/zxjc_2.txt"):
	map[re.sub('\（.*?\）', '', re.sub('\(.*?\)', '', line.strip().split(" ")[0]))] = True
fileinput.close()
file = open("organized/huanjing/zxjc_poi.txt","w")
for k,v in map.iteritems():
	addr = k.replace("#","")
	res = json.loads(urllib2.urlopen(urllib2.Request("http://api.map.baidu.com/geocoder?address="+addr+"&output=json&key=hIlimGuvEfHV41Aw885gONzB&city=杭州")).read())
	poi = str(res["result"]["location"]["lng"])+","+str(res["result"]["location"]["lat"]) if res.has_key("result") and len(res["result"])==4 else "None"
	print addr, poi
	file.write(addr+"\t"+poi+"\n")
file.close()

### step B ####
map = {}
for line in fileinput.input("organized/huanjing/zxjc_poi.txt"):
	part = line.strip().split("\t")
	map[part[0]] = part[1]
fileinput.close()
file = open("data/huanjing/zxjc_2.txt","w")
for line in fileinput.input("organized/huanjing/zxjc_2.txt"):
	part = line.strip().split(" ")
	addr, tm, info = re.sub('\（.*?\）', '', re.sub('\(.*?\)', '', part[0])).replace("#",""), part[-1], "\t".join(part[1:-1])
	poi = map[addr]
	if tm != "-":
		file.write(tm+"\t"+addr+"\t"+poi+"\t"+info+"\n")
fileinput.close()
file.close()

map = {}
for line in fileinput.input("organized/luwang/hzjtydzs_poi.txt"):
	part = line.strip().split(" ")
	map[part[0]] = part[1]
fileinput.close()
file = open("data/luwang/hzjtydzs.txt","w")
for line in fileinput.input("organized/luwang/hzjtydzs_uniq.txt"):
	road = line.strip().split("\t")[1].split(" ")[0]
	if map.has_key(road):
		file.write(map[road]+"\t"+line)
fileinput.close()
file.close()

file = open("data/xiaoqu/ganji_xiaoqu_info.txt","w")
for line in fileinput.input("organized/xiaoqu/ganji_xiaoqu_info.txt"):
	part = line.strip().split("\t")
	file.write(part[10]+"\t"+"\t".join(part[1:9])+"\t"+"\t".join(part[9].split(" "))+"\t".join(part[11:])+"\n")
fileinput.close()
file.close()

map = {}
for line in fileinput.input("organized/xiaoqu/ganji_xiaoqu_info.txt"):
	part = line.strip().split("\t")
	map[part[1]] = part[10]
fileinput.close()
file1 = open("data/xiaoqu/ganji_xiaoqu_unit_chuzu.txt","w")
file2 = open("data/xiaoqu/ganji_xiaoqu_unit_ershou.txt","w")
for line in fileinput.input("organized/xiaoqu/ganji_xiaoqu_unit.txt"):
	part = line.strip().split("\t")
	tp, name, info, price = part[1], part[2], part[3], part[4]
	if not map.has_key(name):
		continue
	poi = map[name]
	if tp == "chuzu":
		file1.write(poi+"\t"+name+"\t"+"\t".join(info.strip().split(", "))+"\t"+price+"\n")
	if tp == "ershou":
		file2.write(poi+"\t"+name+"\t"+"\t".join(info.strip().split(" ")[0].split(","))+"\t"+price+"\n")
fileinput.close()
file1.close()
file2.close()

file = open("data/xuexiao/sxue_info.txt","w")
for line in fileinput.input("organized/xuexiao/sxue_info.txt"):
	part = line.strip().split("\t")
	s1 = re.findall('属性: (.*?) ', part[0])[0] if len(re.findall('属性: (.*?) ', part[0]))!=0 and ":" not in re.findall('属性: (.*?) ', part[0])[0] else "None"
	s2 = re.findall('性质: (.*?) ', part[0])[0] if len(re.findall('性质: (.*?) ', part[0]))!=0 and ":" not in re.findall('性质: (.*?) ', part[0])[0] else "None"
	s3 = re.findall('类型: (.*?) ', part[0])[0] if len(re.findall('类型: (.*?) ', part[0]))!=0 and ":" not in re.findall('类型: (.*?) ', part[0])[0] else "None"
	file.write(part[4]+"\t"+part[3]+"\t"+part[0].split(" ")[0]+"\t"+s1+"\t"+s2+"\t"+s3+"\t"+part[1]+"\t"+part[2]+"\n")
fileinput.close()
file.close()

file = open("data/yiyuan/ganji_yiyuan_info.txt","w")
for line in fileinput.input("organized/yiyuan/ganji_yiyuan_info.txt"):
	part = line.strip().split("\t")
	file.write(part[2]+"\t"+part[1]+"\t"+part[3]+"\n")
fileinput.close()
file.close()
