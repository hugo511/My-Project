# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 16:00:37 2018

@author: Hugo Xian
"""
import jieba
import pickle 
#from collections import Counter
from gensim import corpora,models,similarities
#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import TfidfTransformer
#from collections import  defaultdict 
f1=open('E:\Dissertation\TextP\puretext_xy2.pickle','rb')
dataset=pickle.load(f1)
f1.close

"""
content1=dataset['x'][1]                           
cut=jieba.cut(content1)
cutword=[x for x in cut]
highfreq=Counter(cutword).most_common()
#print("/".join(cutword))
"""
total_cutword_x=[[word for word in jieba.cut(dataset['case_x'][i])] for i in range(0,len(dataset['case_x']))]#
test_case_x=[word for word in jieba.cut(dataset['case_x'][5])]
"""
count_vectorizer=CountVectorizer(min_df=50)
word_matrix_x=count_vectorizer.fit_transform(total_cutword_x[:])
x_matrix=word_matrix_x.toarray() 
x_vo_dict=count_vectorizer.vocabulary_  
x_vo_list=count_vectorizer.get_feature_names()
"""
x_dictionary=corpora.Dictionary(total_cutword_x)
x_dictionary.filter_extremes(no_below=50);len(x_dictionary)
xxdic=[word for word in x_dictionary.token2id]
xxfre=[fre for fre in x_dictionary.dfs]
x_corpus=[x_dictionary.doc2bow(case) for case in total_cutword_x] ##将语料库表示为向量
"""
frequency=defaultdict(int)
for text in total_cutword_x:
    for token in text:
        frequency[token]+=1
texts=[ [ token for token in text if frequency[token] > 5 ] for text in total_cutword_x]
"""
test_case_vec=x_dictionary.doc2bow(test_case_x)
tf_idf=models.TfidfModel(x_corpus)
case_vector=tf_idf[x_corpus]

index = similarities.SparseMatrixSimilarity(tf_idf[x_corpus], num_features=len(x_dictionary.keys()))
sim = index[tf_idf[test_case_vec]]
similarity=sorted(enumerate(sim), key=lambda item: -item[1])#[0:20]
deletecase=[];
for s in range(0,len(similarity)):
    if similarity[s][1]<0.15:
        deletecase.append(similarity[s])
for x in deletecase:
    similarity.remove(x)
#similarity.remove(x for x in deletecase)
simi_text_x_raw=[];simi_text_y=[];
for i in range(0,len(similarity)):
    if youtcome[0][similarity[i][0]] != 0 and youtcome[0][similarity[i][0]] != '*':
        simi_text_x_raw.append(dataset['case_x'][similarity[i][0]]);
        simi_text_y.append(youtcome[0][similarity[i][0]]);
"""
simi_text_x=[dataset['x'][5],dataset['x'][1815],dataset['x'][12972],dataset['x'][3456],dataset['x'][13248]]
simi_text_y=[youtcome[0][5],youtcome[0][1815],youtcome[0][12972],youtcome[0][3456],youtcome[0][13248]]
"""
from sklearn import linear_model
#将文本分成两部分
from sklearn.cross_validation import train_test_split
x_train_raw,x_dev_raw,y_train,y_dev=train_test_split(simi_text_x_raw,simi_text_y,test_size=0.20)
#提取x文本特征向量
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer=TfidfVectorizer(token_pattern='\w', ngram_range=(1,2), max_df=100, min_df=0)
x_train=vectorizer.fit_transform(x_train_raw)
x_dev=vectorizer.transform(x_dev_raw)
#做逻辑回归
clf = linear_model.LogisticRegression(penalty='l2',C=1.0,solver='liblinear',n_jobs=-1).fit(x_train,y_train)
predicted=clf.predict(x_dev)
from sklearn import metrics
print(metrics.classification_report(y_dev, predicted))
#print('accuracy_score: %0.5fs' %(metrics.accuracy_score(y_dev, predicted)))
from sklearn.metrics import roc_auc_score
AUC=roc_auc_score(y_dev, predicted);print ('AUC:%f'%AUC);
#查看逻辑异判案件
import pandas as pd
x_dev_punctuation=pd.DataFrame(columns=['case_x_punctuation','case_x','case_y','name']);
for x_dev_raw_i in x_dev_raw :
    x_dev_punctuation=x_dev_punctuation.append(dataset.loc[dataset.case_x == x_dev_raw_i]);
x_dev_punctuation=x_dev_punctuation.drop_duplicates(subset=['case_x'],keep='first');##初始文本加上
##构造dataframe查看总的结果
data_dev=pd.DataFrame(columns=['case_x_punctuation','case_x','y_dev','y_predicted'])
data_dev['case_x_punctuation']=x_dev_punctuation['case_x_punctuation'].tolist()
data_dev['case_x']=x_dev_punctuation['case_x'].tolist();
data_dev['y_dev']=y_dev;data_dev['y_predicted']=predicted
data_dev.to_excel('E:/Dissertation/TextP/tf-idfv3.xlsx')
