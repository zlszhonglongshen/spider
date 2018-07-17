from pandas import DataFrame, Series
import pandas as pd;
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY, YEARLY
from matplotlib.dates import MonthLocator, MONTHLY
import datetime
import pylab

MA1 = 10  # 移动平均线的日期间隔
MA2 = 50
# '股票代码,名称,收盘价,最高价,最低价,开盘价,前收盘,涨跌额,涨跌幅,换手率,成交量,成交金额,总市值,流通市值
startdate = datetime.date(2017, 8, 1)
enddate = datetime.date(2018, 3, 26)
data = pd.DataFrame(pd.read_excel('eastmoney.xlsx', sheet_name=1, index_col='日期'))  # 读取数据、设置日期为index
data = data.sort_index()  # 按日期升序排列
# 抽取需要的列组成新的表
stdata = pd.DataFrame({'DateTime': data.index, 'Open': data.开盘价, 'High': data.最高价, 'Close': data.收盘价, 'Low': data.最低价})
stdata['DateTime'] = mdates.date2num(stdata['DateTime'].astype(datetime.date))  # 把日期转化成天数，从公元0年开始算


# stdata=stdata.set_index('DateTime')
# stdata.drop(data.columns[6:],axis=1,inplace=True),stdata['Volume']=data.涨跌幅,del stdata['名称']

def main():
    daysreshape = stdata.reset_index()
    daysreshape = daysreshape.reindex(columns=['DateTime', 'Open', 'High', 'Low', 'Close'])

    Av1 = pd.rolling_mean(daysreshape.Close.values, MA1)
    Av2 = pd.rolling_mean(daysreshape.Close.values, MA2)
    SP = len(daysreshape.DateTime.values[MA2 - 1:])
    fig = plt.figure(facecolor='#07000d', figsize=(15, 10))

    ax1 = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4, axisbg='#07000d')
    candlestick_ohlc(ax1, daysreshape.values[-SP:], width=.6, colorup='#ff1717', colordown='#53c156')
    Label1 = str(MA1) + ' SMA'
    Label2 = str(MA2) + ' SMA'

    ax1.plot(daysreshape.DateTime.values[-SP:], Av1[-SP:], '#e1edf9', label=Label1, linewidth=1.5)
    ax1.plot(daysreshape.DateTime.values[-SP:], Av2[-SP:], '#4ee6fd', label=Label2, linewidth=1.5)
    ax1.grid(True, color='w')
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.yaxis.label.set_color("w")
    ax1.spines['bottom'].set_color("#5998ff")
    ax1.spines['top'].set_color("#5998ff")
    ax1.spines['left'].set_color("#5998ff")
    ax1.spines['right'].set_color("#5998ff")
    ax1.tick_params(axis='y', colors='w')
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax1.tick_params(axis='x', colors='w')
    plt.ylabel('Stock price and Volume')
    plt.show()


if __name__ == "__main__":
    main()