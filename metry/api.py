#coding:utf-8

import urllib2
from lxml import etree
import json
import random
import sys
import re
import json
import time
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from user_agents import agents
reload(sys)
sys.setdefaultencoding('utf8')



def get_json2(date,rk,CK,r,nowe,start,end):
    '''根据构造出的url获取到航班数据'''
    url='http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1=%s&ACity1=%s&SearchType=S&DDate1=%s&IsNearAirportRecommond=0&rk=%s&CK=%s&r=%s'%(start,end,date,rk,CK,r)
    headers={'Host':"flights.ctrip.com"}
    headers['User-Agent']=random.choice(agents)
    headers['Referer']="http://flights.ctrip.com/booking/%s-%s-day-1.html?ddate1=%s"%(start,end,date)
    req=urllib2.Request(url,headers=headers)
    res=urllib2.urlopen(req)
    data=res.read()
    #print(data)
    sleeptime = (1, 2, 3, 4, 5,6, 1, 2, 1, 3, 1, 4)
    time.sleep(random.choice(sleeptime))
    dict_content=json.loads(data,encoding="gb2312")
    print len(dict_content['fis']) 
    fis = dict_content['fis']
    for fi in fis:
            flight = fi['fn']
            fly_time = fi['dt']
            arrival_time = fi['at']
            fly_station = fi['dpbn']
            arrival_station = fi['apbn']
            depart_brigdge = json.loads(fi['confort'])['DepartBridge']
            History_Punctuality = json.loads(fi['confort'])['HistoryPunctuality']
            tax = fi['tax']
            print(u"flight",flight)
            print(u"departure time",fly_time)
            print(u"arrive time",arrival_time)
            print(u"liangqiaolv",depart_brigdge)
            print(u"punctuality",History_Punctuality)
            print(u"flystation",fly_station)
            print(u"arrivalstation",arrival_station)
            print(u"minghangfazhanjijing",tax)
            prices = fi['scs']
            for price in prices:
                alt_price = price['salep']
                print(u"alt_price",alt_price)
            print("==================================================")
def get_parameter(date):
    '''获取重要的参数
    date:日期，格式示例：2016-05-13
    '''
    url='http://flights.ctrip.com/booking/hrb-sha-day-1.html?ddate1=%s'%date
    res=urllib2.urlopen(url).read()
    tree=etree.HTML(res)
    pp=tree.xpath('''//body/script[1]/text()''')[0].split()
    CK_original=pp[3][-34:-2]
    CK=CK_original[0:5]+CK_original[13]+CK_original[5:13]+CK_original[14:]

    rk=pp[-1][18:24]
    num=random.random()*10
    num_str="%.15f"%num
    rk=num_str+rk
    r=pp[-1][27:len(pp[-1])-3]

    return rk,CK,r


def enter():
    now = datetime.now()
    #group = ['SHA','KMG','BJS','CTU','CAN','SZX','CKG']
    group = ['SHA','CTU']
    for start in group:
        for end in group:
            if start == end:
                pass
            else:
                i = 0
                while i < 30:
                    timespan = timedelta(days=i)
                    n_days = now + timespan
                    i = i + 1
                    querytime = n_days.strftime('%Y-%m-%d')
                    nowe = now.strftime('%Y-%m-%d')
                    rk,CK,r = get_parameter(querytime)
                    get_json2(querytime,rk,CK,r,nowe,start,end)
    allendtime = datetime.now()
    print("-----------------end time-------------------------")
    print (allendtime - allstarttime).seconds

if __name__=='__main__':
    enter()
