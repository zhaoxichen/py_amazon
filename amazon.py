# coding=utf-8
'''
Created on 2016-8-16
@author: Jennifer
Project:使用chrome浏览器，安装chromewebdriver.exe
'''

from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://www.amazon.com')
# 输入，搜索
print('输入关键字   dog  ,搜索...')
driver.find_element_by_id('twotabsearchtextbox').send_keys('dog')
driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input').click()
products_a_list = driver.find_elements_by_xpath('//*[@id="s-results-list-atf"]/li/div/div[2]/div/a/img')
print(len(products_a_list))
my_product_pic = 'https://images-na.ssl-images-amazon.com/images/I/51TVi1hDoVL._AC_US200_.jpg'
count = 0
for a in products_a_list:
    count += 1
    pic = a.get_attribute('src');
    if my_product_pic == pic:
        print('我的商品在>>>' + str(count) + '位')
    print(a.get_attribute('src'))

driver.quit()
