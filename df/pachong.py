# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 14:40:38 2018

@author: dell
"""


def huoqu_sanji(url):
    list_code = []
    list_name = []
    #firefox_profile = webdriver.FirefoxProfile()
    #firefox_profile.set_preference('permissions.default.image', 2)  # 某些firefox只需要这个
    # firefox_profile.set_preference('browser.migration.version', 9001)#部分需要加上这个
    # 禁用css
    # firefox_profile.set_preference('permissions.default.stylesheet', 2)
    # 禁用flash
    # firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    driver = webdriver.PhantomJS(executable_path=r'C:\Users\dell\Desktop\phantomjs-2.1.1-windows\bin\phantomjs')
    #driver = webdriver.Firefox(executable_path=r'C:\Program Files\Mozilla Firefox\geckodriver',
    #                           firefox_profile=firefox_profile)
    driver.implicitly_wait(8)
    # url = 'http://quote.eastmoney.com/center/boardlist.html#boards-BK08541'
    driver.get(url=url)
    data = driver.page_source
    soup = BeautifulSoup(data, "html.parser")
    if soup.find_all(id='main-table_paginate_page')[0].find_all('a'):
        nums = soup.find_all(id='main-table_paginate_page')[0]
        num = int(nums.find_all('a')[-1].get_text())
        page = 0;
        while page < num:

            data = driver.page_source
            soup = BeautifulSoup(data, "html.parser")
            table = soup.find_all(id='main-table')[0]
            body = table.find_all('tbody')[0]

            for tr in body.find_all('tr', class_='odd'):
                code = tr.find_all('td')[1].get_text()
                list_code.append(code)
                wz = tr.find_all('td')[1]('a')[0]['href']
                name = tr.find_all('td')[2].get_text()
                list_name.append(name)
                # print(code,wz,name)
            for tr in body.find_all('tr', class_='even'):
                code = tr.find_all('td')[1].get_text()
                list_code.append(code)
                wz = tr.find_all('td')[1]('a')[0]['href']
                name = tr.find_all('td')[2].get_text()
                list_name.append(name)
                print(code, wz, name)
            driver.find_element_by_xpath('//*[@id="main-table_next"]').click()
            page = page + 1
            # print('-------',page)
            time.sleep(4)  #
    else:

        table = soup.find_all(id='main-table')[0]
        body = table.find_all('tbody')[0]

        for tr in body.find_all('tr', class_='odd'):
            code = tr.find_all('td')[1].get_text()
            list_code.append(code)
            wz = tr.find_all('td')[1]('a')[0]['href']
            name = tr.find_all('td')[2].get_text()
            list_name.append(name)
            # print(code,wz,name)
        for tr in body.find_all('tr', class_='even'):
            code = tr.find_all('td')[1].get_text()
            list_code.append(code)
            wz = tr.find_all('td')[1]('a')[0]['href']
            name = tr.find_all('td')[2].get_text()
            list_name.append(name)
            # print(code,wz,name)
    driver.close()
    return list_name, list_code


import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import pymysql.cursors
import pymysql
import datetime

connection = pymysql.connect(host='58edd9c77adb6.bj.cdb.myqcloud.com',
                             port=5432,
                             user='root',
                             password='1160329981wang',
                             db='qianmancang',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
# def huoqu_yiji:(url):
# firefox_profile = webdriver.FirefoxProfile()
# firefox_profile.set_preference('permissions.default.image', 2)
# firefox_profile.set_preference('browser.migration.version', 9001)
# 禁用css
# firefox_profile.set_preference('permissions.default.stylesheet', 2)
# 禁用flash
# firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
driver = webdriver.PhantomJS(executable_path=r'C:\Users\dell\Desktop\phantomjs-2.1.1-windows\bin\phantomjs')
# driver = webdriver.Firefox(executable_path=r'C:\Program Files\Mozilla Firefox\geckodriver',
#                            firefox_profile=firefox_profile)
taday = datetime.date.today()
list_urls = []
url = 'http://quote.eastmoney.com/center/boardlist.html#concept_board'

driver.get(url=url)
data = driver.page_source
# htm2 = urllib.request.urlopen(html)
# data.encoding = 'utf-8'
soup = BeautifulSoup(data, "html.parser")
nums = soup.find_all(id='main-table_paginate_page')[0]
num = int(nums.find_all('a')[-1].get_text())
page = 0;
while page < num:

    data = driver.page_source
    soups = BeautifulSoup(data, "html.parser")
    bodys = soups.find_all(id='main-table')[0]
    body = bodys.find_all('tbody')[0]
    for tr in body.find_all('tr', class_='odd'):
        name_gainian = tr.find_all('td')[1].get_text()
        wz = tr.find_all('td')[1]('a')[0]['href']
        print(name_gainian, wz)
        url = 'http://quote.eastmoney.com' + wz
        html = requests.get(url)
        html.encoding = 'utf-8'
        soups = BeautifulSoup(html.text, "html.parser")
        bodyss = soups.find_all('div', class_='side_box phase_increases lineHeightTb')[0]
        urls_1 = bodyss.find_all('a', class_='more fr')[0]['href']
        # print(urls)
        try:
            a, b = huoqu_sanji(urls_1)
        except:
            print('wrong', urls_1)
            list_urls.append(urls_1)
        print('aaaaaaaaaaaaaaa', a, b)
        for name, code in zip(a, b):
            print('---', name, code, name_gainian, taday)
            try:
                with connection.cursor() as cursor:

                    # 执行sql语句，插入记录
                    SQL = """insert into gainian(name,code,gainian,date)
                    values
                    (%s, %s, %s, %s)"""
                    cursor.execute(SQL, (name, code, name_gainian, taday))
                    # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                    connection.commit()
            except Exception as e:
                print('***** Logging failed with this error:', str(e))
    for tn in body.find_all('tr', class_='even'):
        name_gainian = tn.find_all('td')[1].get_text()
        wzs = tn.find_all('td')[1]('a')[0]['href']
        # print('even',name_gainian,wz)
        url_2 = 'http://quote.eastmoney.com' + wzs
        html = requests.get(url_2)
        html.encoding = 'utf-8'
        soups = BeautifulSoup(html.text, "html.parser")
        bodyss = soups.find_all('div', class_='side_box phase_increases lineHeightTb')[0]
        urls_2 = bodyss.find_all('a', class_='more fr')[0]['href']
        # print(urls)
        try:
            c, d = huoqu_sanji(urls_2)
        except:
            print('wrong', urls_2)
            list_urls.append(urls_2)
        print('ccccccc', c)
        # list_name = a+c
        # list_code = b+d
        for name, code in zip(c, d):
            print('---', name, code, name_gainian, taday)
            try:
                with connection.cursor() as cursor:

                    # 执行sql语句，插入记录
                    SQL = """insert into gainian(name,code,gainian,date)
                    values
                    (%s, %s, %s, %s)"""
                    cursor.execute(SQL, (name, code, name_gainian, taday))
                    # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                    connection.commit()
            except Exception as e:
                print('***** Logging failed with this error:', str(e))
    driver.find_element_by_xpath('//*[@id="main-table_next"]').click()
    page = page + 1
    print('-------', page)
    time.sleep(8)  #
driver.close()


