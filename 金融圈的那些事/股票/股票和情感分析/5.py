import pandas as pd
import matplotlib.pyplot as plt

data1 = pd.read_excel('sentiment.xlsx', sheet_name=0)
data1 = data1.fillna(method='pad')  # 因为周末没开盘，所以用周五的价格填充，保证画图连续性
# newdata=pd.merge(data1,data2,how='left',left_on='date',right_on='日期')
x = data1.date
y1 = data1.pos
y2 = data1.price
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(x, y1)
ax1.set_ylabel('sitiment')
ax1.set_title("Sentiment")
ax1.legend(loc='upper right')

ax2 = ax1.twinx()  # 设置双y轴
ax2.plot(x, y2, 'r')
ax2.set_ylabel('stock price')
ax2.set_xlabel('date')
ax2.legend(loc='upper left')
plt.show()