#coding:utf-8
'''
任务：
今天有一个需求，是每天统计出参加银联扫码活动的商家信息，主扫的交易笔数，总金额，被扫的交易笔数，总金额，以及主扫+被扫的统计信息。
分析：首先要做个程序，每天跑一下就生成结果文件，或者直接显示出结果。涉及到的有：
1、使用cx_oracle查询，获取数据，数据存入本地文件或者显示到ui的文本框/标签中。
2、打算不再使用tkinter，转用很强大的qt库，pyqt5，来做界面
3、引入日历控件，这样就不用用户手动输出日期了，直接在日历上点选就可以啦
4、多做异常捕获，应对用户可能出现的各种错误操作
5、由于统计任务很耗时间（银联每日数据量很大），所以要把界面线程和工作线程分开，这样就不会出现在查询的时候界面死掉的情况

'''
import sys
from PyQt5.QtWidgets import (QWidget, QCalendarWidget, QLabel, QApplication, QPushButton, QGridLayout,QLineEdit,QMessageBox)
from PyQt5.QtCore import QDate,QThread,pyqtSignal
from PyQt5.QtGui import QIcon
import cx_Oracle
import datetime
import time
import os

# 工作线程类，继承自PyQt5.QtCore里的QThread类，只要重写init和run方法（init可以不重写）就可以实现我们自己的多线程了，不懂的参考我的一篇Python多线程文章：http://blog.csdn.net/drdairen/article/details/60962439
# 和qt多线程大同小异

class runthread(QThread):
    _signal = pyqtSignal(list)
    def __init__(self, parent = None):
        super(runthread, self).__init__()
        self.dstr=""
    def __del__(self):
        self.wait()
    def setvalue (self,daystr):#在界面线程中调用，用来传入日期参数
        self.dstr = daystr
        #print(self.dstr)

    def run(self):#重写的run方法，实现查询的工作，传出参数为msg列表
        day_str=self.dstr
        msg = []
        msg.append(day_str)
        try:
            conn=self.connect_oracle()
        except:
            msg.append("error_conn")
            self._signal.emit(msg)
            return
        mcursor=conn.cursor()

        sql_tab_exist = "select * from BSA_%s where rownum<2"%day_str
        try:
            mcursor.execute(sql_tab_exist)
            laji=mcursor.fetchall()
        except:
            msg.append("error_tab")
            self._signal.emit(msg)
            return

        sql01 = "t" % day_str#保密起见，删除了所有的sql语句内容
        mcursor.execute(sql01)
        row1 = mcursor.fetchone()

        data_a = row1[0]
        data_b = row1[1]
        msg.append(data_a)
        msg.append(data_b)



        sql02 = #保密起见，删除了所有的sql语句内容
        mcursor.execute(sql02)
        row2 = mcursor.fetchone()
        data_c = row2[0]
        data_d = row2[1]
        msg.append(data_c)
        msg.append(data_d)

        sql03 = #保密起见，删除了所有的sql语句内容
        mcursor.execute(sql03)
        row3 = mcursor.fetchone()
        data_e = row3[0]
        msg.append(data_e)

        mcursor.close()
        conn.commit()
        conn.close()
        self._signal.emit(msg)
    def connect_oracle(self):#专门连接oracle的函数
        try:
            conn = cx_Oracle.connect(#保密起见，删除了所有的保密语句内容')
            #print("connect success!")
        except:
            #print("connect error!")
            pass
        return conn

class Example(QWidget):#界面线程类，继承自QWidget类
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):#初始化界面

        grid = QGridLayout()
        grid.setSpacing(10)
        self.setLayout(grid)

        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        # cal.move(20, 20)
        grid.addWidget(self.cal, 1, 0)
        self.cal.clicked[QDate].connect(self.showDate)
        #信号槽链接到显示日期的函数

        self.lbl = QLabel(self)
        grid.addWidget(self.lbl, 1, 2)
        date = self.cal.selectedDate()
        self.lbl.setText(str(date.toPyDate()))
        # self.lbl.move(130, 260)


        self.lbl02 = QLabel(self)
        grid.addWidget(self.lbl02, 1, 1)
        self.lbl02.setText("您选择的日期是：")
        # self.lbl.move(130, 260)


        self.btn = QPushButton('开始查询', self)
        # self.btn.move(100, 100)
        grid.addWidget(self.btn, 2, 2)
        self.btn.clicked.connect(self.run_select)#信号槽连接到开始任务的函数

        lab01 = QLabel('二维码主扫笔数：')
        lab02 = QLabel('二维码主扫金额(元)：')

        lab03 = QLabel('二维码被扫笔数：')
        lab04 = QLabel('二维码被扫金额(元)：')

        lab05 = QLabel('二维码活跃商户数：')

        grid.addWidget(lab01, 3, 0)
        grid.addWidget(lab02, 4, 0)
        grid.addWidget(lab03, 5, 0)
        grid.addWidget(lab04, 6, 0)
        grid.addWidget(lab05, 7, 0)

        self.lab1 = QLineEdit(self)
        self.lab2 = QLineEdit(self)
        self.lab3 = QLineEdit(self)
        self.lab4 = QLineEdit(self)
        self.lab5 = QLineEdit(self)

        self.lab1.setText("")
        self.lab2.setText("")
        self.lab3.setText("")
        self.lab4.setText("")
        self.lab5.setText("")

        grid.addWidget(self.lab1, 3, 1)
        grid.addWidget(self.lab2, 4, 1)
        grid.addWidget(self.lab3, 5, 1)
        grid.addWidget(self.lab4, 6, 1)
        grid.addWidget(self.lab5, 7, 1)

        self.setGeometry(300, 200, 500, 300)
        self.setWindowTitle('二维码活动每日商户统计')
        self.setWindowIcon(QIcon('C:\\Program Files\\1.PNG'))
        #图标，百度上找了个银联的图标，哈哈
        self.show()

    def run_select(self):

        self.lab1.setText("")
        self.lab2.setText("")
        self.lab3.setText("")
        self.lab4.setText("")
        self.lab5.setText("")

        date = self.cal.selectedDate()
        format_date = str(date.toPyDate())
        day_str=self.strp_time(format_date)

        self.thread = runthread()

        self.thread.setvalue(day_str)
        self.thread._signal.connect(self.show_result)
        self.thread.start()


        #self.close()
    def show_result (self,msg):
        if msg[1] == "error_tab":
            QMessageBox.information(self, '错误！', "%s 的数据还未导入！" % msg[0])
            return
        elif msg[1] == "error_conn":
            QMessageBox.information(self, '错误！', "数据库连接失败！！" % msg[0])
            return
        #print(msg)
        self.lab1.setText(str(msg[1]))
        self.lab2.setText(str(msg[2] / 100.00))
        self.lab3.setText(str(msg[3]))
        self.lab4.setText(str(msg[4] / 100.00))
        self.lab5.setText(str(msg[5]))
        QMessageBox.information(self, '提示！', "%s 的数据已经查询完毕！" % msg[0])
    def strp_time(self,begin_date):#从格式化的日期中剥出我要用的日期字符串
        begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
        date_str = begin_date.strftime("%Y%m%d")
        return date_str
    def showDate(self, date):
        datestring = str(date.toPyDate())
        self.lbl.setText(datestring)
        # self.lbl.setText(date.toString())
    def closeEvent(self, event):#用户点x关掉界面的时候，会警告
        reply = QMessageBox.question(self, '警告！',"Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())