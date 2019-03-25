# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 10:40:43 2018

@author: Hugo Xian
"""
import requests
import pickle
from bs4 import BeautifulSoup
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from IPAPI import get_IP4
import random

for j in range(28,29):  #缺9.19？11.6,7 12.13[:1000]
    proxiespool=get_IP4()
    if j <= 9:
        n=str(j).zfill(2)
        date='2017-12-%s'%str(n)
    else:
        date='2017-12-%s'%str(j)
#def get_content(date):
    fl=open('E:\Dissertation\WSPJ\db_foradayv2\db_for_con_aday{0}.pickle'.format(date),'rb')
    database1=pickle.load(fl)
    fl.close
    s=requests.Session()
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    print('第{0}天共有{1}条请求要获取'.format(date,len(database1['DocId'])))
    for i in range(1400,1561):  #len(database1['DocId'])
        if database1['DocId'][i]=='':
            database1['content'].append('缺少id')
        else:
            ctnurl='http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={0}'.format(database1['DocId'][i])
            header = {'Host':'wenshu.court.gov.cn',
              'Origin':'http://wenshu.court.gov.cn',
             #'Referer':'http://wenshu.court.gov.cn/content/content?DocID={0}&KeyWord='.format(database1['DocId'][i]),
              'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
             # 'Connection':'keep-alive'
            }
            content_proxies={'https':'http://'+random.choice(proxiespool)}
            try:
                ctnreq=s.get(ctnurl,headers=header,verify=False,proxies=content_proxies)
                pat0='(?<=案件名称":").*?(?=")'
                html=ctnreq.text
                if '360安域' in html or html =='[]\n':
                    database1['content'].append('null')
                    print('第%d条获取正文出错'%i)
                    #time.sleep(1)
                else:
                    bf=BeautifulSoup(html,'html.parser')
                    title=re.compile(pat0).findall(html)
                    content=str(title)+('\n')
                    for k in bf.find_all('div'):
                        s3=k.get_text()
                        content=content+s3
                    if content =='[]\n':
                        database1['content'].append('null')
                        print('第%d条获取正文出错'%i,'提交验证码以继续')
                        input_kb=input()
                        if input_kb=='m':
                            break
                    else:
                        database1['content'].append(content)
                        print('第%d条正文获取完毕'%i)
            except:
                print('chunk mistake')
                database1['content'].append('null')
            #print(ctnreq.text)
   # print('第{0}天共有{1}条请求要获取'.format(date,len(database1['DocId'])))
    fl=open('E:\Dissertation\WSPJ\db_foradayv2_content\db_content_tot.pickle'.format(date),'rb')
    db_content_tot=pickle.load(fl)
    fl.close   
    for i in range(0,len(database1['content'])):
        db_content_tot['DocId'].append(database1['DocId'][i])
        db_content_tot['date'].append(database1['date'][i])
        db_content_tot['name'].append(database1['name'][i])
        db_content_tot['trail'].append(database1['trail'][i])
        db_content_tot['casenum'].append(database1['casenum'][i])
        db_content_tot['crtname'].append(database1['crtname'][i])
        db_content_tot['content'].append(database1['content'][i]) #
    fl=open('E:\Dissertation\WSPJ\db_foradayv2_content\db_content_tot.pickle','wb')
    pickle.dump(db_content_tot,fl)
    fl.close
    print('第{0}天已保存'.format(date))
###保存日文件    
    fl=open('E:\Dissertation\WSPJ\db_foradayv2_content\db_for_con_aday{0}_1.pickle'.format(date),'wb')
    pickle.dump(database1,fl)
    fl.close    
                          
###写入总的文件
#db_content_tot=dict({'DocId':[],'date':[],'name':[],'trail':[],'casenum':[],'crtname':[],'content':[]})
