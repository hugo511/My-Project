# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 22:47:05 2019

@author: Hugo Xian
"""

"""
rs = open('E:/Project/Adult Analysis/adultData_Test.csv', 'w')
 
with open('E:/Project/Adult Analysis/adultData_Test.csv') as file:
    for line in file:
        if '?' in line:
            continue
        else:
            rs.write(line)

rs.close()
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
 
import sys
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
 
__author__ = 'Su'
 
"""
算法一：决策树算法(gini系数/entropy信息熵增益)
算法二：随机森林算法(a.10个决策树分支  b.100个决策树分支)
"""
 
names = ("age, workclass, education, education-num, "
         "marital-status, occupation, relationship, race, sex, "
         "capital-gain, capital-loss, hours-per-week, "
         "native-country, income").split(', ')

data = pd.read_csv('E:/Project/Adult Analysis/adultData_Train.csv')
#读取数据预处理后的训练集数据(省略了第二行数据。原因：第二行为编号，不构成数据筛选条件)
data_test = pd.read_csv('E:/Project/Adult Analysis/adultData_Test.csv')
#读取数据预处理后的测试集数据(省略了第二行数据。原因同上)
names = data.columns
# print data.head()
# print data.count()
# print data.describe()
 
for name in ["workclass","education", "marital-status", "occupation", "relationship", "race", "sex", "native-country", "income"]:
    col = pd.factorize(data[name])[0].astype(np.uint16)
    data[name]=col
#文本属性转数组
 
for name in ["workclass","education", "marital-status", "occupation", "relationship", "race", "sex", "native-country", "income"]:
    col1 = pd.factorize(data_test[name])[0].astype(np.uint16)
    data_test[name]=col1
#文本属性转数组
 
# print data
 
X_train = data[['age','workclass','education','education-num','marital-status','occupation','relationship','race','sex','capital-gain','capital-loss','hours-per-week','native-country']]
#训练集X
y_train = data[['income']]
#训练集y
 
X_test = data_test[['age','workclass','education','education-num','marital-status','occupation','relationship','race','sex','capital-gain','capital-loss','hours-per-week','native-country']]
#测试集X
y_test = data_test[['income']]
#测试集y
 
# print X_test.head()
# print y_test.head()
 
# print X_train.head()
# print y_train.head()
 
from sklearn import preprocessing
#sklearn数据标准化函数
 
"""
公式为：(X-mean)/std  计算时对每个属性/每列分别进行。
将数据按期属性（按列进行）减去其均值，并处以其方差。得到的结果是，对于每个属性/每列来说所有数据都聚集在0附近，方差为1。
"""
 
# X = np.array(data)
# X_scaled = preprocessing.scale(X)
 
X_train = preprocessing.scale(np.array(X_train))
y_train = np.array(y_train)
X_test = preprocessing.scale(np.array(X_test))
y_test = np.array(y_test)
 
from sklearn import tree
 
clf = tree.DecisionTreeClassifier(criterion='gini')
clf = clf.fit(X_train,y_train)
 
#entropy
clf_entropy = tree.DecisionTreeClassifier(criterion='entropy')
clf_entropy = clf_entropy.fit(X_train,y_train)
 
print (clf.score(X_test,y_test))
#准确率  0.805976095618  gini系数
 
print (clf_entropy.score(X_test,y_test))
#准确率  0.808100929615  信息熵增益
 
 
X_train_cov = np.cov(X_train.T)
X_train_eig = np.linalg.eig(X_train_cov)
# print X_train_eig
#上面三行是主成成分分析(PCA)，各项特征值(下面的特征值矩阵)均未达到可以忽略不计的地步，故保留所有属性
 
"""
array([ 2.08371954,  0.38413677,  1.40465934,  0.60817972,  0.69172145,
        1.12767226,  0.83234406,  0.85438115,  1.09623844,  0.91510361,
        0.96803332,  0.99929443,  1.03494693])
"""
 
from sklearn.ensemble import RandomForestClassifier
clf2 = RandomForestClassifier(n_estimators=10)
clf3 = RandomForestClassifier(n_estimators=100)
clf2 = clf2.fit(X_train,y_train)
clf3 = clf3.fit(X_train,y_train)
 
print (clf2.score(X_test,y_test))
#准确率  0.836387782205  10个决策树
 
print (clf3.score(X_test,y_test))
#准确率  0.840571049137  100个决策树
