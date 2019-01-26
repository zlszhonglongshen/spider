# -*- coding: utf-8 -*-
"""
Created on 2019-01-26 13:23
@author: Johnson
Email:593956670@qq.com
@software: PyCharm
"""
def list_to_txt(list,file_name):
    file = open("./"+file_name+'.txt','w')
    for i in list:
        k = ' '.join([str(j) for j in i])
        file.write(k+"\n")
    file.close()

