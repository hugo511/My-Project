
import urllib
import http.cookiejar as cookielib
import re
import execjs
import random
import ssl
import requests
import json
from urllib import parse
import pickle
from crawl_ip import crawlip
#from IPAPI import get_IP2
#from IPAPI import get_IP3
from IPAPI import get_IP4
import uuid
import datetime
import time

proxiespool=get_IP4()
s=requests.Session()
Url="http://wenshu.court.gov.cn"
urllist="http://wenshu.court.gov.cn/list/list/?sorttype=1&number=A3EXFTV7&guid=a4103106-1934-74f9c684-59d9b84f84e1&conditions=searchWord+1+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6&conditions=searchWord+%E6%B5%99%E6%B1%9F%E7%9C%81+++%E6%B3%95%E9%99%A2%E5%9C%B0%E5%9F%9F:%E6%B5%99%E6%B1%9F%E7%9C%81"
agent_pool=["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
        "Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.2; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"]

def get_vjkl5():
    url1 = "http://wenshu.court.gov.cn/list/list/?sorttype=1&number=A3EXFTV7&guid=a4103106-1934-74f9c684-59d9b84f84e1&conditions=searchWord+1+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6&conditions=searchWord+%E6%B5%99%E6%B1%9F%E7%9C%81+++%E6%B3%95%E9%99%A2%E5%9C%B0%E5%9F%9F:%E6%B5%99%E6%B1%9F%E7%9C%81"
    #Referer1 = url1
    headers1 = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Host":"wenshu.court.gov.cn",
            "Proxy-Connection":"keep-alive",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
        }
    req1 = s.get(url=url1,headers=headers1)
    vjkl5 = req1.cookies["vjkl5"]
    print("vjkl5:"+str(vjkl5))
    return (vjkl5)

def get_guid():
    guid=uuid.uuid4()
    print ("guid:"+str(guid))
    return(guid)

def get_vl5x(vjkl5):
    fh=open('E:/Dissertation/WSPJ/base64.js','r')
    js1=fh.read()
    fh.close()
    fh=open('E:/Dissertation/WSPJ/md5.js','r')
    js2=fh.read()
    fh.close()
    fh=open('E:/Dissertation/WSPJ/getkey3.js','r')
    js3=fh.read()
    fh.close()
    fh=open('E:/Dissertation/WSPJ/sha1.js','r')
    js4=fh.read()
    fh.close()
    js_all=js1+js2+js3+js4
    js_all=js_all.replace("ce7c8849dffea151c0179187f85efc9751115a7b",str(vjkl5))
    ctx=execjs.compile(js_all)
    vl5x=ctx.call("getKey",str(vjkl5))
    print ("vl5x:"+str(vl5x))
    return(vl5x)

def getnumb(guid):
    urlgetcode="http://wenshu.court.gov.cn/ValiCode/GetCode"
    codedata={"guid":guid}
    num_headers={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
                 'Host':'wenshu.court.gov.cn',
                'Origin':'http://wenshu.court.gov.cn',
                'Referer':'http://wenshu.court.gov.cn/',
                'X-Requested-With':'XMLHttpRequest',}
    res1=s.post(urlgetcode,codedata,headers=num_headers)
    number=res1.text
    print(number)
    return (number)
#number=getnumb(guid)
def gettreecontent(Paramstr,vl5x,guid,number,vjkl5):
    trdata=urllib.parse.urlencode({"Param":Paramstr,
                 "vl5x":vl5x,
                 "guid":guid,
                 "number":str(number)})
    trurl="http://wenshu.court.gov.cn/List/TreeContent"
    trheaders = {
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"en,zh-CN;q=0.9,zh;q=0.8",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Host":"wenshu.court.gov.cn",
        "Origin":"https://wenshu.court.gov.cn",
        "Proxy-Connection":"keep-alive",
        "Cookie":"vjkl5="+vjkl5,
        "Referer":"http://wenshu.court.gov.cn/list/list/?sorttype=1&number={0}&guid={1}&conditions=searchWord+QWJS+++{2}".format(number,guid,parse.quote(Paramstr)),
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest",
        }
    trproxies={'https':'https://'+random.choice(proxiespool)}  #删除了random.choice()2018.10.06
    trresp=s.post(url=trurl,headers=trheaders,data=trdata,proxies=trproxies)
    #print(resp.text)
    if trresp.text == '"remind"' or trresp.text == '"remind key"' :
        return('获取目录树出错')
    else:
        json_data=json.loads(trresp.text.replace('\\','').replace('"[','[').replace(']"',']'))   
        tree_dict={}
        for type_data in json_data:  
            type_name = type_data['Key']
            type_dict = {'IntValue': type_data['IntValue'],'ParamList': []}
            for data in type_data['Child']:
                if data['IntValue']:
                    type_dict['ParamList'].append({'Key':data['Key'],'IntValue':data['IntValue']})
            tree_dict[type_name] = type_dict
        return (tree_dict)

def savedatav2(real_list1):
    try:
        for i in range(0,len(real_list1)):
           database_total['date'].append(real_list1[i][1])
           database_total['name'].append(real_list1[i][2])
           database_total['DocId'].append(real_list1[i][3])
           database_total['trail'].append(real_list1[i][4])
           database_total['casenum'].append(real_list1[i][5])
           database_total['crtname'].append(real_list1[i][6])
    except:
       pass
        
def get_docid2(listcontent):
    apiurl='http://www.ulaw.top:5677/crack'
    s=requests.Session()
    return_str=s.post(apiurl,data={'a':listcontent})
    try:
        real_list=eval(return_str.content)
        return(real_list)
    except:
            print('解密获取出错')
            time.sleep(8)
    

def getlist(Paramstr,guid,vl5x):
    number=getnumb(guid)
    for i in range(0,10):
        url2="http://wenshu.court.gov.cn/List/ListContent"
        datal=urllib.parse.urlencode({"Param":Paramstr,
                                  "Index":str(i+1),
                                  "Page":"20",
                                  "Order":"法院层级",
                                  "Direction":"asc",
                                  "number":str(number),                                 
                                  "guid":guid,
                                  "vl5x":vl5x,
                                  }).encode('utf-8')
        agent_pool=["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
                "Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.2; .NET4.0E)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"]
        liheaders={"Accept": "*/*",
                 "User-Agent":random.choice(agent_pool),
                 "Referer":"http://wenshu.court.gov.cn/list/list/?sorttype=1&number={0}&guid={1}&conditions=searchWord+QWJS+++{2}".format(number,guid,parse.quote(Paramstr)),
                 "Host":"wenshu.court.gov.cn",
                 "Connection":"keep-alive",
                 "Proxy-Connection":"keep-alive",
                 "Origin": "https://wenshu.court.gov.cn",
                 "X-Requested-With":"XMLHttpRequest",
                 "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                 "Cookie": "vjkl5="+vjkl5,
                 }
        ssl._create_default_https_context = ssl._create_unverified_context
        li_proxies={'https':'https://'+random.choice(proxiespool)}  #删除了random.choice  10.06
        pagelist=s.post(url2,datal,headers=liheaders,proxies=li_proxies,timeout=120)
        if pagelist.text == '':
            break
        elif '抱歉' in pagelist.text:
            print('第%d页出错'%(i+1))
        else:
            try:  
                real_pagelist=get_docid2(pagelist.text)
                savedatav2(real_pagelist)
                #print('第%d页爬取完毕'%(i+1))
            except:
                print('第%d页出错'%(i+1))
    
#读取之前爬取结果
"""
fl=open('db_for_con_aday0624-0625.pickle','rb')
database=pickle.load(fl)
print('爬取之前条数为%d'%len(database['name']))
"""
start=datetime.date(2017,9,30);
end=datetime.date(2017,9,30);
delta_date=datetime.timedelta(days=1)
delta_date2=datetime.timedelta(days=1)
d=start
while d <= end: 
    database_total=dict({'runeval':[],'DocId':[],'date':[],'name':[],'trail':[],'casenum':[],'crtname':[],'content':[]})
    in_roop_end=d+delta_date2
    vjkl5=get_vjkl5()
    guid=get_guid()
    vl5x=get_vl5x(vjkl5)
    number=getnumb(guid)
    while d < in_roop_end:
        start_date=d.strftime('%Y-%m-%d')
        """
        case_process_list = ['一审', '二审', '再审', '非诉执行审查', '再审审查与审判监督','其他']
        court_type=['最高法院','高级法院','中级法院','基层法院']
        wenshu_type_list = ['裁判书', '调解书', '决定书', '通知书', '批复', '答复','函', '令', '其他']
        """
        Paramstr="案件类型:行政案件,裁判日期:{0} TO {1}".format(start_date,start_date)
        tr_num=gettreecontent(Paramstr,vl5x,guid,number,vjkl5)
        while tr_num == "获取目录树出错" or len(tr_num) == 0:
            tr_num=gettreecontent(Paramstr,vl5x,guid,number,vjkl5)    #判断请求是否成功，不成功重新请求
        if tr_num['裁判年份']['IntValue'] <= 200 :
            getlist(Paramstr,guid,vl5x)
        else:
            for i in range(0,len(tr_num['文书类型']['ParamList'])):
                Paramstr2=Paramstr+',文书类型:'+tr_num['文书类型']['ParamList'][i]['Key']    #second_order_con
                if tr_num['文书类型']['ParamList'][i]['IntValue'] <= 200 :
                    getlist(Paramstr2,guid,vl5x)
                else : 
                    tr_num3=gettreecontent(Paramstr2,vl5x,guid,number,vjkl5)
                    while tr_num3 == "获取目录树出错" or len(tr_num3) == 0:
                        tr_num3=gettreecontent(Paramstr2,vl5x,guid,number,vjkl5)   #判断请求是否成功，不成功重新请求
                    for j in range(0,len(tr_num3['审判程序']['ParamList'])):
                        Paramstr3=Paramstr2+',审判程序:'+tr_num3['审判程序']['ParamList'][j]['Key']    #third_order_con
                        if tr_num3['审判程序']['ParamList'][j]['IntValue'] <= 200 :
                            getlist(Paramstr3,guid,vl5x)          
                        else:
                            tr_num4=gettreecontent(Paramstr3,vl5x,guid,number,vjkl5)
                            while tr_num4 == "获取目录树出错" or len(tr_num4) == 0 :
                                tr_num4=gettreecontent(Paramstr3,vl5x,guid,number,vjkl5)  #判断请求是否成功，不成功重新请求
                            for q in range(0,len(tr_num4['法院层级']['ParamList'])):
                                Paramstr4=Paramstr3+',法院层级:'+tr_num4['法院层级']['ParamList'][q]['Key']   #fourth_order_con
                                getlist(Paramstr4,guid,vl5x)
        print ('日期%s爬取完毕'%start_date)
        print ('案例数:%d'%len(database_total['name']))
        d+=delta_date  #加一天

        fl=open('E:\Dissertation\WSPJ\db_foradayv2\db_for_con_aday{0}.pickle'.format(start_date),'wb')  ##实际数据到：06-27
        pickle.dump(database_total,fl)
        fl.close
        
    print('进入睡眠40min')
    #time.sleep(2400)  #睡眠40min



        
        
        

"""
fl=open('db_for_con_aday0628.pickle','wb')  ##实际数据到：06-27
pickle.dump(database,fl)
fl.close
"""
