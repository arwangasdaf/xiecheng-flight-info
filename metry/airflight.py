#!/usr/bin/python
# -*- coding: UTF-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from threading import Timer
from selenium.common.exceptions import TimeoutException
# 引入ActionChains鼠标操作类
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime, timedelta
import sys
import random
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
# 引入配置对象DesiredCapabilities
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

allstarttime = datetime.now()


def html(driver, start, end, now, querytime):
    url = "http://flights.ctrip.com/booking/" + start + "-" + end + "-day-1.html?DDate1=" + querytime

    # time.sleep(random.uniform(20,40))
    driver.get(url)
    print("get-------------------")
    # driver.get("http://flights.ctrip.com/booking/SHA-CAN-day-1.html?DDate1=2017-10-26")
    # target = driver.find_element_by_class_name("data_travelsky")
    # driver.execute_script("arguments[0].scrollIntoView();", target)
    # time.sleep(15)
    try:
        driver.execute_script("window.scrollBy(0,10000)")
        time.sleep(3)
        driver.execute_script("window.scrollBy(0,20000)")
        time.sleep(3)
        driver.execute_script("window.scrollBy(0,30000)")
        time.sleep(3)
        driver.execute_script("window.scrollBy(0,40000)")
        time.sleep(5)
    except Exception:
        print("******************error********************************")

    pageSource = driver.page_source
    html_parse = BeautifulSoup(pageSource, "lxml")
    # 拿到所有的航班的div
    temp = html_parse.findAll("div", "search_box_light")
    print("get temp")
    if temp is None:
        print("-------cant find---------")
    else:
        for div in temp:
            company = ""
            companynode = div.find("strong", "flight_logo")
            if companynode is None:
                company = "0"
            else:
                company = companynode.get_text()

            hangban = ""
            hangbannode = div.find("div", "J_flight_no")
            if hangbannode is None:
                hangban = "0"
            else:
                hangbannode1 = hangbannode.find("span")
                if hangbannode1 is None:
                    hangban = "0"
                else:
                    hangban = hangbannode1.get_text()

            start_time = ""
            starttimenode = div.find("td", "right")
            if starttimenode is None:
                start_time = "0"
            else:
                starttimenode1 = starttimenode.find("strong", "time")
                if starttimenode1 is None:
                    start_time = "0"
                else:
                    start_time = starttimenode1.get_text()

            end_time = ""
            endtimenode = div.find("td", "left")
            if endtimenode is None:
                end_time = "0"
            else:
                endtimenode1 = endtimenode.find("strong", "time")
                if endtimenode1 is None:
                    end_time = "0"
                else:
                    end_time = endtimenode1.get_text()

            jixing = ""
            jixingnode = div.find("div", "J_flight_no")
            if jixingnode is None:
                jixing = "0"
            else:
                jixingnode1 = jixingnode.find("span")
                if jixingnode1 is None:
                    jixing = "0"
                else:
                    jixingnode2 = jixingnode1.find_next("span")
                    if jixingnode2 is None:
                        jixing = "0"
                    else:
                        jixing = jixingnode2.get_text()

            start_airport = ""
            startnode = div.find("td", "right")
            if startnode is None:
                start_airport = "0"
            else:
                startnode1 = startnode.find("strong", "time")
                if startnode1 is None:
                    start_airport = "0"
                else:
                    startnode2 = startnode1.find_next("div")
                    if startnode2 is None:
                        start_airport = "0"
                    else:
                        start_airport = startnode2.get_text()

            end_airport = ""
            endnode = div.find("td", "left")
            if endnode is None:
                end_airport = "0"
            else:
                endnode1 = endnode.find("strong", "time")
                if endnode1 is None:
                    end_airport = "0"
                else:
                    endnode2 = endnode1.find_next("div")
                    if endnode2 is None:
                        end_airport = "0"
                    else:
                        end_airport = endnode2.get_text()

            zhundianlv = ""
            zhnode = div.find("span", "J_punctuality")
            if zhnode is None:
                zhundianlv = "0"
            else:
                zhundianlv = zhnode.get_text()

            price = ""
            pricenode = div.find("span", "base_price02")
            if pricenode is None:
                price = "0"
            else:
                price = pricenode.get_text()

            if jixing == u"共享":
                print("filter----" + jixing)
            else:
                # mation = company +"  "+hangban+"  "+ jixing +"  "+ start_time + "  " + end_time+ "  " + start_airport + "  "+ end_airport +"  "+zhundianlv +"  "+ price +"  " + time + "  " + querytime
                mation = u'%s,%s,%s,%s,%s,%s，%s,%s,%s,%s,%s,%s,%s' % (
                start, end, company, hangban, jixing, start_time, end_time, start_airport, end_airport, zhundianlv,
                price, now, querytime)
                dtime = datetime.now().strftime("%Y-%m-%d-%H")
                txtname = dtime + '.txt'
                a = open(txtname, 'a')
                a.write(str(mation.encode('utf-8')))
                a.write('\n')
                print("mation------")
                # print(mation)
                print(hangban)
                print("*******************write**************************")
                a.close()
                # print(company +"  "+hangban+"  "+ jixing +"  "+ start_time + "  " + end_time+ "  " + start_airport + "  "+ end_airport +"  "+zhundianlv +"  "+ price +"  " + time + "  " + querytime)


def enter():
    now = datetime.now()
    group = ['SHA','KMG','BJS','CTU','CAN','SZX','CKG']
    #group = ['SHA', 'KMG', 'BJS']
    service_args = []
    service_args.append('--load-images=no')
    service_args.append('--ignore-ssl-errors=true')
    # driver = webdriver.PhantomJS()
    for start in group:
        for end in group:
            if start == end:
                pass
            else:
                i = 0
                print(start)
                print(end)
                driver = webdriver.PhantomJS()
                while i < 30:
                    timespan = timedelta(days=i)
                    n_days = now + timespan
                    i = i + 1
                    querytime = n_days.strftime('%Y-%m-%d')
                    nowe = now.strftime('%Y-%m-%d')
                    html(driver, start, end, nowe, querytime)
                try:
                    driver.quit()
                except Exception:
                    print("exception")
                print("fffffffffffffffffffffffffffffffffffff")
    allendtime = datetime.now()
    print("-----------------end time-------------------------")
    print (allendtime - allstarttime).seconds
    enter()


if __name__ == '__main__':
    enter()

