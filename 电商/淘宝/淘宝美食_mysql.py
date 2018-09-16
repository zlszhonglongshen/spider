#coding:utf-8

import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import pymongo
import pymysql

KEYWORD = "苹果手机"

conn = pymysql.connect(host="172.20.71.35",
                       port=3306,
                       user="root",
                       passwd="Infinitus_2018",
                       db="mysql",
                       charset="utf8mb4")
cursor = conn.cursor()
sql1 = """CREATE TABLE taobao (
        image CHAR(250) ,
        price CHAR(250),
        deal CHAR(250),
         title CHAR(250),
        shop CHAR(250),
        location CHAR(250))"""
cursor.execute(sql1)






SERVICE_ARGS = ['--load-images=false','--disk-cache=true'] #参数
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
wait = WebDriverWait(browser, 10)

browser.set_window_size(1400, 900)

def search():
    print('正在搜索')
    try:
        browser.get('https://www.taobao.com')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        input.send_keys(KEYWORD)
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return total.text
    except TimeoutException:
        return search()


def next_page(page_number):
    print('正在翻页', page_number)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)


def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        # print(item)
        try:
            image = str(item.find('.pic .img').attr('src'))
            price = str(item.find('.price').text())
            deal = str(item.find('.deal-cnt').text()[:-3])
            title = str(item.find('.title').text())
            shop = str(item.find('.shop').text())
            location = str(item.find('.location').text())
            sql2 = ("INSERT INTO taobao(image,price,deal,title,shop ,location)" "VALUES(%s,%s,%s,%s,%s,%s)")
            cursor.execute(sql2,(image,price,deal,title,shop,location))
            conn.commit()
        except Exception  as e:
            print("导入失败！！！")

        # print(title)
def main():
    try:
        total = search()
        total = int(re.compile('(\d+)').search(total).group(1))
        for i in range(2, total + 1):
            next_page(i)
    except Exception:
        print('出错啦')
    finally:
        browser.close()

if __name__ == '__main__':
    main()