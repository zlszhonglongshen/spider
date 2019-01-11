#coding=utf-8
import json
import urllib.request
import time
import traceback
#模拟成浏览器
headers={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
         "Accept-Encoding":"gbk,utf-8,gb2312",
         "Accept-Language":"zh-CN,zh;q=0.8",
         "User-Agent":"Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
         "Connection":"keep-alive"}
opener=urllib.request.build_opener()
headall=[]
for key,value in headers.items():
    item=(key,value)
    headall.append(item)
opener.addheaders=headall
#将opener安装为全局
urllib.request.install_opener(opener)
#构造数据，城市分别是北京、天津、石家庄、太原、济南、沈阳、呼和浩特、郑州
city_id = ['54511','54517','53698','53772','54823','54342','53463','57083']
def getcityid(city):
    if city == 'beijing':
        return city_id[0]
    elif city == 'tianjin':
        return city_id[1]
    elif city == 'shijiazhuang':
        return city_id[2]
    elif city == 'taiyuan':
        return city_id[3]
    elif city == 'jinan':
        return city_id[4]
    elif city == 'shenyang':
        return city_id[5]
    elif city == 'huhehaote':
        return city_id[6]
    else:
        return city_id[7]
def getweather(city):
    try:
        url = "http://www.nmc.cn/f/rest/real/"+getcityid(city)
        stdout = urllib.request.urlopen(url)
        weatherInfo = stdout.read().decode('utf-8')
        jsonData = json.loads(weatherInfo)
        # print(jsonData)
        weatherlist = []
        # 读取JSON数据，添加到列表中
        szDate = jsonData["publish_time"]
        weatherlist.append(szDate)
        szCity = jsonData["station"]["city"]
        print("城市: "+str(szCity))
        szWeather = jsonData["weather"]["info"]
        weatherlist.append(szWeather)
        szdirect = jsonData["wind"]["direct"]
        weatherlist.append(szdirect)
        szspeed = str(jsonData["wind"]["speed"]) + "m/s"
        weatherlist.append(szspeed)
        szTemp = str(jsonData["weather"]["temperature"]) + "℃"
        weatherlist.append(szTemp)
        szhumidity = str(int(jsonData["weather"]["humidity"])) + "%"
        weatherlist.append(szhumidity)
        szairpressure = str(jsonData["weather"]["airpressure"])
        weatherlist.append(szairpressure)
        szalert = str(jsonData["warn"]["alert"])
        weatherlist.append(szalert)
        szfmeans = str(jsonData["warn"]["fmeans"])
        weatherlist.append(szfmeans)
        print("数据更新时间，天气，风向，风速，实时温度，相对湿度,大气压,预警,温馨提示：")
        print(weatherlist)
        writefiles_weather(city,weatherlist)
    except urllib.error.URLError as e:
        print("获取天气状况数据出现URLERROR！一分钟后重试……")
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        time.sleep(60)
        # 出现异常则过一段时间重新执行此部分
        getweather(city)
    except Exception as e:
        print("获取天气状况数据出现EXCEPTION！十秒钟后重试……")
        print("Exception：" + str(e))
        traceback.print_exc()  # 获得错误行数
        time.sleep(10)
        # 出现异常则过一段时间重新执行此部分
        getweather(city)
def writefiles_weather(filename,weatherlist):
    try:
        #将获取的数据写入文件中，数据分别为数据更新时间，天气，风向，风速（m/s），实时温度（℃），相对湿度（%）。
        with open("D:\data_weather_"+filename+".txt","a",errors="ignore") as f:
            for weather in weatherlist:
                f.write(str(weather))
                f.write(",")
            f.write("\n")
        print("该条天气数据已添加到文件中！")
    except Exception as e:
        print("天气状况数据写入文件函数出现异常！将跳过此部分……")
        print("Exception："+str(e))
        traceback.print_exc()  #获得错误行数
        pass
if __name__ == '__main__':
    while(True):
        print("==========开始工作==========")
        getweather("beijing")
        getweather("tianjin")
        getweather("shijiazhuang")
        getweather("taiyuan")
        getweather("jinan")
        getweather("shenyang")
        getweather("huhehaote")
        getweather("zhengzhou")
        #休息一小时
        print("【休息中……】")
        time.sleep(3600)