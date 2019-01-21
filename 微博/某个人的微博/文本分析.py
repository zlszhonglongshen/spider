'''
@Coding: 
@Author: Johnson
@Date: 2019-01-21 13:53:46
@Description: 
@Email: 593956670@qq.com
'''
#参考网址：https://blog.csdn.net/qq_41888542/article/details/81143170

# -*- coding: utf-8 -*-
import fool
from collections import Counter
from PIL import Image,ImageSequence  
from wordcloud import WordCloud,ImageColorGenerator
 
#因留言结构比较乱，所以先保存到本地做进一步处理
pd.DataFrame(comment).to_csv(r"C:\Users\zhangjunhong\Desktop\comment.csv")
 
#处理完以后再次载入进来
comment_data = pd.read_excel(r"C:\Users\zhangjunhong\Desktop\comment.xlsx")
 
#将数据转换成字符串
text = (",").join(comment_data[0])
 
#进行分词
cut_text = ' '.join(fool.cut(text))
 
#将分词结果进行计数
c = Counter(cut_text)
c.most_common(500)#挑选出词频最高的500词
 
#将结果导出到本地进行再一次清洗,删除一些符号词
pd.DataFrame(c.most_common(500)).to_excel(r"C:\Users\zhangjunhong\Desktop\fenci.xlsx")
 
 
image = Image.open('C:/Users/zhangjunhong/Desktop/图片1.png')#作为背景形状的图  
graph = np.array(image)  
#参数分别是指定字体、背景颜色、最大的词的大小、使用给定图作为背景形状  
wc = WordCloud(font_path = "C:\\Windows\\Fonts\\simkai.ttf", background_color = 'White', max_words = 150, mask = graph)  
 
fp = pd.read_csv(r"C:\Users\zhangjunhong\Desktop\da200.csv",encoding = "gbk")#读取词频文件  
name = list(fp.name)#词  
value = fp.time#词的频率   
dic = dict(zip(name, value))#词频以字典形式存储  
wc.generate_from_frequencies(dic)#根据给定词频生成词云 
image_color = ImageColorGenerator(graph)  
plt.imshow(wc)  
plt.axis("off")#不显示坐标轴  
plt.show() 
wc.to_file('C:/Users/zhangjunhong/Desktop/wordcloud.jpg')
