# encoding=utf-8
import jieba
import jieba.analyse as al
import thulac


file_object = open('sina_fin.txt')
try:
     all_the_text = file_object.read( )
finally:
     file_object.close( )



#seg_list = jieba.cut(all_the_text, cut_all=True)
#print("Full Mode: " + "/ ".join(seg_list))  # 全模式

#seg_list = jieba.cut(all_the_text, cut_all=False)
#print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
jieba.suggest_freq('计划',False)
seg_list = jieba.cut(all_the_text)  # 默认是精确模式
print(",".join(seg_list))

#seg_list = jieba.cut_for_search(all_the_text)  # 搜索引擎模式
## print(", ".join(seg_list))

#al.set_stop_words('stop_word.txt')
all_the_text="明天，我想去天安门，我想去上海和北京"
tags=al.extract_tags(all_the_text,topK=100,withWeight=False)
print len(tags)
print (",".join(tags))
#for item in tags:
#     print item[0],item[1]
tl = thulac.thulac(seg_only=True,filt=True)  #默认模式
text = tl.cut("明天，我想去天安门，我想去上海和北京", text=False)  #进行一句话分词
print text[0]


import matplotlib.pyplot as plt
from wordcloud import WordCloud

text_from_file_with_apath = open('sina_fin.txt').read()



wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all = True)
wl_space_split = " ".join(wordlist_after_jieba)

print text_from_file_with_apath
my_wordcloud = WordCloud().generate(wordlist_after_jieba)

#plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
#plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()