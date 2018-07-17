from datetime import datetime
from pylab import *
import matplotlib.dates as mdates
import dateutil, pylab, random
from pylab import *

import matplotlib.pyplot as plt

data = pd.DataFrame(pd.read_excel('sentiment.xlsx'))
data.columns = ['date', 'positive', 'confidence', 'sentiments']
newdata = data.groupby('date').agg(lambda x: list(x))  ## 相同日期的聚一起

times = []
sentiment = []
for i in range(1, newdata.shape[0]):
    p = newdata.positive[i]
    d = newdata.index[i]
    sum = 0
    for z in p:
        sum += z
    average = sum / len(p)
    times.append(d)
    sentiment.append(average)
pylab.plot_date(pylab.date2num(times), sentiment, linestyle='-')
xtext = xlabel('time')
ytext = ylabel('sentiments')
ttext = title('sentiments')
grid(True)
setp(ttext, size='large', color='r')