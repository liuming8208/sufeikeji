# -*- coding: utf-8 -*-

import ssl,time
from selenium import webdriver

ssl._create_default_https_context = ssl._create_unverified_context
executable_path = "/Users/liuming/Desktop/Tool/python/geckodriver"

def login():

    driver = webdriver.Firefox(executable_path=executable_path)
    driver.set_page_load_timeout(10)

    driver.get("https://message.sufeikeji.com/login/index")  #登录

    driver.find_element_by_name('LoginForm[account]').send_keys('')  #用户名
    driver.find_element_by_name('LoginForm[password]').send_keys('') #密码

    time.sleep(1)

    driver.find_element_by_xpath('//button[@class="btn btn-primary block full-width m-b"]').click()  #提交按钮
    time.sleep(1)

    # 信息不准确页面
    driver.get("http://test1.phoenixtree.com.cn/inaccurate-info")

    time.sleep(2)
    
    driver.find_element_by_name('sekProject').send_keys('捷翔饮品')
    driver.find_element_by_xpath('//a[@class="easyui-linkbutton l-btn l-btn-small"]').click() #提交按钮

    time.sleep(2)

    driver.find_element_by_name('sekOrg').send_keys('君联资本')
    driver.find_element_by_xpath('//a[@class="easyui-linkbutton l-btn l-btn-small"]').click()

    driver.execute_script('$("#sekBath").combobox("setValue",1)') #赋值easy_ui 界面combobox框值
    time.sleep(1)
    driver.find_element_by_xpath('//a[@class="easyui-linkbutton l-btn l-btn-small"]').click()

    time.sleep(4)
    driver.execute_script('$("#sekBath").combobox("setValue",2)')
    time.sleep(1)
    driver.find_element_by_xpath('//a[@class="easyui-linkbutton l-btn l-btn-small"]').click()

    driver.find_element_by_name('sekProject').clear()  #清除input框里面的内容
    driver.find_element_by_name('sekOrg').clear()

    time.sleep(2)
    driver.execute_script('$("#sekBath").combobox("setValue",1)')
    time.sleep(2)
    driver.find_element_by_name('sekStime').send_keys('2018-01-01')
    driver.find_element_by_xpath('//a[@class="easyui-linkbutton l-btn l-btn-small"]').click()

    time.sleep(4)
    driver.find_element_by_name('sekEtime').send_keys('2018-01-02')
    driver.find_element_by_xpath('//a[@class="easyui-linkbutton l-btn l-btn-small"]').click()


if __name__ == '__main__':

    login()







