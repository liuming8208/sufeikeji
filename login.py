# -*- coding: utf-8 -*-

import ssl,time
from selenium import webdriver

ssl._create_default_https_context = ssl._create_unverified_context
executable_path = "/Users/liuming/Desktop/Tool/python/geckodriver"

def login():

    driver = webdriver.Firefox(executable_path=executable_path)
    driver.set_page_load_timeout(10)

    driver.get("http://localhost/login/index")  #登录

    driver.find_element_by_name('LoginForm[username]').send_keys('liuming')  #用户名
    #time.sleep(1)
    driver.find_element_by_name('LoginForm[password]').send_keys('xxxx') #密码
    driver.find_element_by_name("login-button").click()
    time.sleep(1)

    driver.get("http://localhost/site/organization")  # 机构
    # time.sleep(8)
    #
    # driver.get("http://localhost/site/company")  # 公司
    # time.sleep(4)
    #
    # driver.get("http://localhost/site/event")  # 事件
    # time.sleep(4)
    #
    # driver.get("http://localhost/site/member")  # 成员
    # time.sleep(4)
    #
    # driver.get("http://localhost/site/export")  # 导出
    # time.sleep(2)
    #
    # driver.get("http://localhost/site/craw")  # 数据
    # time.sleep(2)
    #
    # driver.get("http://localhost/site/organization")  # 机构
    # time.sleep(2)

    driver.find_element_by_id('qt_name').send_keys('国开金诚')
    driver.find_element_by_id('qt_btn_search').click()

    time.sleep(1)
    driver.find_element_by_id('it_name').send_keys('中植资本')
    driver.find_element_by_id('it_btn_search').click()

    time.sleep(1)
    driver.find_element_by_name("add_start_time").send_keys('2018-01-26')
    driver.find_element_by_id('it_btn_search').click()

    driver.find_element_by_id('it_name').clear()
    driver.find_element_by_name("add_start_time").clear()
    time.sleep(3)
    driver.find_element_by_name("add_start_time").send_keys('2018-01-22')
    driver.find_element_by_name("add_end_time").send_keys('2018-01-23')
    driver.find_element_by_id('it_btn_search').click()

if __name__ == '__main__':

    login()







