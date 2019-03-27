# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 13:57:15 2018

@author: Hugo Xian
"""
import re
import pickle

fl=open('E:\Dissertation\TextP\dataset.pickle','rb')
dataset=pickle.load(fl)
fl.close
###选出判决书
data_judge={'name':[],'content':[]}
pat0="(?<=\[').*?(?='\])"
for i in range(0,len(dataset['content'])):#
    try:
        title=re.compile(pat0).findall(dataset['content'][i])
        #print(title)
        if '判决书' in title[0]:
            data_judge['content'].append(dataset['content'][i])
            data_judge['name'].append(dataset['name'][i])
    except:
        pass

fl=open('E:\Dissertation\TextP\data_judge.pickle','wb')
pickle.dump(data_judge,fl)
fl.close

##分离案情和判决结果
fl=open('E:\Dissertation\TextP\data_judge.pickle','rb')
data_judge=pickle.load(fl)
fl.close

pat1="(?<=\n).*?(?=\u5224\u51b3\u5982\u4e0b)" #依照行政诉讼法
pat2="(?<=\u5224\u51b3\u5982\u4e0b).*(?=\u5ba1.{0,5}\u5224)"  #审判
pat3="\D{4}\u5e74\D{1,2}\u6708\D{1,3}\u65e5?" ##年月日
case={'name':[],'x':[],'y':[]}
xerr=[];yerr=[];derr=[]
for i in range(0,len(data_judge['content'])):
    try:
        X=re.compile(pat1).findall(data_judge['content'][i])
        date=re.compile(pat3).findall(data_judge['content'][i])
        if date !='':
            case['x'].append(X[0]+date[0][:-1])       
        case['name'].append(data_judge['name'][i])
    except:
        case['x'].append('null')
        case['name'].append(data_judge['name'][i])
        xerr.append(i)
    try:
        Y=re.compile(pat2).findall(data_judge['content'][i])
        case['y'].append(Y[0])
    except:
        case['y'].append('null')
        yerr.append(i)
   
"""    
for i in range(16,len(yerr)):
    if yerr[i] != xerr[i]:
        print(i)
        break
pat21="(?<=\u5224\u51b3\u5982\u4e0b).*(?=\u6cd5\u5b98\u52a9\u7406)" #法官助理
case['y'][7119]=re.compile(pat21).findall(data_judge['content'][7119])[0]
for i in range(0,len(case['x'])):
    if case['x'][i] == 'null':
        xerr.append(i)
for i in range(0,len(case['y'])):
    if case['y'][i] == 'null':
        yerr.append(i)   
"""
for i in range(0,len(case['x'])):
    if case['x'][i] == 'null' and case['y'][i]== 'null':
        del case['name'][i]
        del case['x'][i]
        del case['y'][i]
        
fl=open('E:\Dissertation\TextP\case_xy.pickle','wb')
pickle.dump(case,fl)
fl.close    

####删除标点符号及乱码
def submark(strings):
    a=strings
    b=re.sub("[{0} ,\.\!\"\#$%&'()*\+\-/:;<=>?@[\]^_`~ * \[ \]×�\(\) a-zA-Z ]+".format(punctuation), "",a)   
    d=re.compile(r"\d+\.?\d*").findall(b) 
    e=re.compile(r"\d+\.?\d*(?=[\u5143|\u4e07])").findall(b)
    for i in e:
        if i in d:
            d.remove(i)
    for i in d:
        b=re.sub(r"(?<=\D)%s(?=\D)"%i,"",b)
    return b
from zhon.hanzi import punctuation  

import re
f1=open('E:\Dissertation\TextP\case_xy.pickle','rb')
dataset=pickle.load(f1)
f1.close
for i in range(0, len(dataset['x'])):
    contentx=dataset['x'][i]
    contenty=dataset['y'][i]
    stringx=submark(contentx)
    stringy=submark(contenty)
    dataset['x'][i]=stringx
    dataset['y'][i]=stringy
#[{0}{1} * \[ \]×�\(\) a-zA-Z \d+\b(?!\u5143) \d+\b(?!\u5341) \d+\b(?!\u5341) \d+\b(?!\u767e) \d+\b(?!\u4e07) \d+\b(?!\u4ebf)]+".format(punctuation,string.punctuation)
f1=open('E:\Dissertation\TextP\puretext_xy1.pickle','wb')##去除了标点符号
pickle.dump(dataset,f1)
f1.close
"""   
x1=dataset['x'][0]    
x2=re.sub("[%s * \[ \]×�]+"%punctuation, "",x1)    
"""
###将原文本和出文本放在一起以便索引
f1=open('E:\Dissertation\TextP\puretext_xy1.pickle','rb')
dataset=pickle.load(f1)
f1.close
f1=open('E:\Dissertation\TextP\case_xy.pickle','rb')
dataset1=pickle.load(f1)
f1.close
data_tot={'case_x_punctuation':dataset1['x'],'case_x':dataset['x'],'case_y':dataset['y'],'name':dataset['name']}
import pandas as pd
df_total=pd.DataFrame(data_tot)
f1=open('E:\Dissertation\TextP\puretext_xy2.pickle','wb')##原文本和纯文本数据文件
pickle.dump(df_total,f1)
f1.close