
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver




class hanshusss:
    def __init__(self,url):
        self.url = url
    def huoqu(self):
        list_code = []
        list_name = []
        list_urls = []
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)  # 某些firefox只需要这个
        # firefox_profile.set_preference('browser.migration.version', 9001)#部分需要加上这个
        # 禁用css
        # firefox_profile.set_preference('permissions.default.stylesheet', 2)
        # 禁用flash
        # firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        # driver = webdriver.PhantomJS(executable_path=r'C:\Users\dell\Desktop\phantomjs-2.1.1-windows\bin\phantomjs')
        driver = webdriver.Firefox(executable_path=r'C:\Program Files\Mozilla Firefox\geckodriver',
                                   firefox_profile=firefox_profile)
        driver.implicitly_wait(4)
        # url = 'http://quote.eastmoney.com/center/boardlist.html#boards-BK08541'
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        try:
            driver.get(self.url)
        except:
            list_urls.append(self.url)
            driver.execute_script('window.stop()')
        #driver.get(self.url)
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