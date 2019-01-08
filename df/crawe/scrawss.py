#import df.hanshu as hss
#import df.mysqlxie as mx
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import pymysql.cursors
import pymysql
import datetime
from df import hanshu as hss
from df import mysqlxie as msql
from df.hanshu import hanshusss
from df.xieru import mysql_xie
#huo = hss.hanshus()
def crawe():
    # my_connection = msql.xiemysql('58edd9c77adb6.bj.cdb.myqcloud.com',
    #                    5432,'root','1160329981wang','qianmancang','utf8mb4',pymysql.cursors.DictCursor)
    # connection = my_connection.connections()
    # def huoqu_yiji:(url):
    # firefox_profile = webdriver.FirefoxProfile()
    # firefox_profile.set_preference('permissions.default.image', 2)
    # firefox_profile.set_preference('browser.migration.version', 9001)#部分需要加上这个
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
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)
    try:
        driver.get(url=url)
    except:
        list_urls.append(url)
        driver.execute_script('window.stop()')
    #driver.get(url=url)
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
            print(urls_1)
            #try:
            huo = hanshusss(urls_1)
            a, b = huo.huoqu()
            # except:
            #     print('wrong', urls_1)
            #     list_urls.append(urls_1)
            print('aaaaaaaaaaaaaaa', a, b)
            for name, code in zip(a, b):
                print('---', name, code, name_gainian, taday)
                my_gainian = mysql_xie(name, code, name_gainian, taday)
                my_gainian.xie_gainian()
                # try:
                #     with connection.cursor() as cursor:
                #
                #         # 执行sql语句，插入记录
                #         SQL = """insert into gainian(name,code,gainian,date)
                #         values
                #         (%s, %s, %s, %s)"""
                #         cursor.execute(SQL, (name, code, name_gainian, taday))
                #         # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                #         connection.commit()
                # except Exception as e:
                #     print('***** Logging failed with this error:', str(e))
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
            #try:
            huos = hanshusss(urls_2)
            c, d = huos.huoqu()

            # except:
            #     print('wrong', urls_2)
            #     list_urls.append(urls_2)
            print('ccccccc', c)
            # list_name = a+c
            # list_code = b+d
            for names, codes in zip(c, d):
                print('---', names, codes, name_gainian, taday)
                my_gainian = mysql_xie(names, codes, name_gainian, taday)
                my_gainian.xie_gainian()
                # try:
                #     with connection.cursor() as cursor:
                #
                #         # 执行sql语句，插入记录
                #         SQL = """insert into gainian(name,code,gainian,date)
                #         values
                #         (%s, %s, %s, %s)"""
                #         cursor.execute(SQL, (names, codes, name_gainian, taday))
                #         # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                #         connection.commit()
                # except Exception as e:
                #     print('***** Logging failed with this error:', str(e))
        driver.find_element_by_xpath('//*[@id="main-table_next"]').click()
        page = page + 1
        print('-------', page)
        time.sleep(8)  #
    driver.close()
if __name__ =='__main__':
    crawe()

