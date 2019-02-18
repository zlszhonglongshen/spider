# -*- coding: utf-8 -*-
"""
Created on 2019/1/25 18:14
@Author: Johnson
@Email:593956670@qq.com
@File: baiduIndex.py
"""
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytesseract
import re
from PIL import Image
import calendar
import time


def get_cookie():
    """
        模拟登陆
        """
    url = 'http://index.baidu.com/'
    driver = webdriver.Chrome(executable_path='C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe')
    driver.get(url)
    time.sleep(30)
    cookies = driver.get_cookies()
    print(cookies)


def init_spider(keyword):
    """
    模拟登陆
    """
    url = 'http://index.baidu.com/'
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get(url)

    COOKIES = 'BAIDUID=15B7F3AE4653F16C918E6EE2AE808C51:FG=1; BIDUPSID=15B7F3AE4653F16C918E6EE2AE808C51; PSTM=1550114140; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; PSINO=6; delPer=0; BDUSS=VuQUpIS1RJTHJaTzlwWkUtLUk2Qkx-bHp0SEFTNWtMVWNyTU5OOUplRUc0STFjQVFBQUFBJCQAAAAAAAAAAAEAAAAZzAAp0MTA5DIwODAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAZTZlwGU2ZcRF; bdindexid=nuj0eigg5u6dlk6nn8hd141k67; BDRCVFR[C0p6oIjvx-c]=I67x6TjHwwYf0; H_PS_PSSID=26523_1457_21106_26350_28414; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PS_REFER=1'
    driver.add_cookie(COOKIES)
    driver.get(url)
    time.sleep(10)
    driver.refresh()
    #输入关键词
    WebDriverWait(driver, 10, 0.5).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class='search-input']")))
    driver.find_element_by_xpath("//input[@class='search-input']").send_keys(keyword)
    WebDriverWait(driver, 10, 0.5).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='search-input-cancle']")))
    driver.find_element_by_xpath("//span[@class='search-input-cancle']").click()
    driver.maximize_window()
    return driver

def aveIndex(driver):
    """
    获取时间段平均指数
    :param driver:
    :return:默认时间段平均指数和时间段
    """
    time.sleep(1)
    WebDriverWait(driver, 10, 0.5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='tabLi gColor1']")))
    driver.find_element_by_xpath("//a[@class='tabLi gColor1']").click()
    time.sleep(3)
    driver.save_screenshot('so.png')
    WebDriverWait(driver, 10, 0.5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="auto_gsid_5"]/div[3]/table/tbody/tr[2]/td[2]/div/span[1]')))
    element=driver.find_element_by_xpath('//*[@id="auto_gsid_5"]/div[3]/table/tbody/tr[2]/td[2]/div/span[1]')
    # 机器识别图片
    image = Image.open("so.png")
    left = element.location.get("x")+20
    top = element.location.get("y")
    right = left + element.size.get("width")+10
    bottom = top + element.size.get("height")
    cropImg = image.crop((left, top, right, bottom))
    cropImg=cropImg.resize((200,20))
    cropImg.save("aveIndex.png")
    number=Image.open('aveIndex.png')
    number=pytesseract.image_to_string(number)

    number=re.sub(r',?\.?\s?:?','',number)
    print(number)

    #时间段
    WebDriverWait(driver, 10, 0.5).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='blkUnit grpUnit']//span[@class='compInfo'][2]")))
    datetime = driver.find_element_by_xpath("//div[@class='blkUnit grpUnit']//span[@class='compInfo'][2]").text
    print(datetime)
    return number,datetime

def getElementImage(driver,element,fromPath,toPath,keyword):
    """
    该元素所对应的截图
    :param element: 元素
    :param fromPath: 图片源
    :param toPath: 截图
    """
    # 找到图片坐标
    locations = element.location
    # 跨浏览器兼容
    scroll = driver.execute_script("return window.scrollY;")
    top = locations['y'] - scroll
    # 找到图片大小
    sizes = element.size
    # 构造关键词长度
    add_length = (len(keyword) - 2) * sizes['width'] / 15
    # 构造指数的位置
    rangle = (
        int(locations['x'] + sizes['width'] / 4 + add_length)-2, int(top + sizes['height'] / 2),
        int(locations['x'] + sizes['width'] * 2 / 3)+2, int(top + sizes['height']))
    time.sleep(2)
    image = Image.open(fromPath)
    cropImg = image.crop(rangle)
    cropImg.save(toPath)

def dailyIndex(driver,x,y,index):
    """
    获取每天的指数
    :param driver:
    :param x: 距离element左上角的横坐标
    :param y: 纵坐标
    :param index: 个
    :return:
    """
    time.sleep(2)
    WebDriverWait(driver, 10, 0.5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#trend > svg > rect')))
    element = driver.find_elements_by_css_selector('#trend > svg > rect')[1]
    time.sleep(2)
    ActionChains(driver).move_to_element_with_offset(element, x, y).perform()
    cot = 0   #viewbox不出现
    while (ExistBox(driver) == False):
        cot += 1
        time.sleep(2)
        y=y+10
        dailyIndex(driver, x, y, index)
        if ExistBox(driver) == True:
            break
        if cot == 6:
            return None
    time.sleep(3)
    driver.get_screenshot_as_file(str(index)+'.png')

    try:
        WebDriverWait(driver, 10, 0.5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@id='viewbox']")))
        datetime=driver.find_element_by_xpath('//*[@id="viewbox"]/div[1]/div[1]').text
        print(datetime)
    except:
        print('次数有误！')
    finally:
        element = driver.find_element_by_xpath("//div[@id='viewbox']")
        getElementImage(driver,element, str(index)+'.png', 'day'+str(index)+'.png',keyword)
        time.sleep(2)
        number = Image.open('day'+str(index)+'.png')
        number = pytesseract.image_to_string(number,lang='fontyp')
        number = re.sub(r',?\.?\s?', '', number)
        number=number.replace('z','2').replace('i','7').replace('e','9')
        print(number)
        return number



#判断ViewBox是否存在
def ExistBox(driver):
    try:
        WebDriverWait(driver, 10, 0.5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@id='viewbox']")))
        return True
    except:
        return False

def defaultIndex(driver):
    """
    获取默认30天的数据和平均数据，最后一天为启动爬虫前一天或两天
    :param keyword:
    :return:
    """
    aveindex,datetime=aveIndex(driver)
    width = 41.68
    x1 = [1]
    x2 = [i * width for i in range(1, 30)]
    x = x1 + x2
    cot = 30
    allIndex=[]
    for i in range(len(x)):
        day=dailyIndex(driver, x[i], cot, i)
        allIndex.append(day)
    return allIndex,aveindex,datetime


'''
第一步获取cookies
第二步将cookies放在列表中
'''

get_cookie()

#多个关键词以逗号隔开
keyword='无限极'
driver = init_spider(keyword)


aveIndex(driver)
defaultIndex(driver)