# -*- coding: utf-8 -*-
"""
Created on 2019/1/18 14:26
@Author: Johnson
@Email:593956670@qq.com
@File: getTime.py
"""
import time
def startPro():
    while(1):
        currentHour = int(time.strftime("%H"))
        print(currentHour)
        if currentHour==7:
            print("It's time")
            break
        if currentHour == 6:
            print("itstimerightnow")
            time.sleep(60)
        else:
            print("It's not time ,sleep........")
            time.sleep(3500)
if __name__ == "__main__":
     startPro()
