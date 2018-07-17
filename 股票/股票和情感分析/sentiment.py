import pandas as pd
import datetime
from aip import AipNlp
import codecs

startdate = datetime.date(2017, 8, 1).strftime('%Y-%m-%d')
enddate = datetime.date(2018, 3, 27).strftime('%Y-%m-%d')
APP_ID = '你的id'
API_KEY = '你的key'
SECRET_KEY = '你的key'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


def get_sentiments(text, dates):
    try:
        sitems = client.sentimentClassify(text)['items'][0]  # 情感分析
        positive = sitems['positive_prob']  # 积极概率
        confidence = sitems['confidence']  # 置信度
        sentiment = sitems['sentiment']  # 0表示消极，1表示中性，2表示积极
        # tagitems = client.commentTag(text, {'type': 9})  # 评论观点
        # propertys=tagitems['prop']#属性
        # adj=tagitems['adj']#描述词
        output = '{}\t{}\t{}\t{}\n'.format(dates, positive, confidence, sentiment)
        f = codecs.open('sentiment.xls', 'a+', 'utf-8')
        f.write(output)
        f.close()
        print('Done')
    except Exception as e:
        print(e)


def get_content():
    data = pd.DataFrame(pd.read_excel('eastmoney.xlsx', sheet_name=0))
    data.columns = ['Dates', 'viewpoints']  # 重设表头
    data = data.sort_values(by=['Dates'])  # 按日期排列
    vdata = data[data.Dates >= startdate]  # 提取对应日期的数据
    newvdata = vdata.groupby('Dates').agg(lambda x: list(x))  # 按日期分组，把同一天的评论并到一起
    return newvdata


viewdata = get_content()
for i in range(viewdata.shape[0]):
    print('正在处理第{}条,还剩{}条'.format(i, viewdata.shape[0] - 1))
    dates = viewdata.index[i]
    for view in viewdata.viewpoints[i]:
        print(view)
        get_sentiments(view,dates)

        
