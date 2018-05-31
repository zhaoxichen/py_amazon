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
print('输入关键字   dog ,搜索...')
driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]').send_keys('dog')
driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input').click()

productUl = driver.find_element_by_id('s-results-list-atf')
lis = productUl.find_elements_by_xpath('li')
print(lis)
# print('总共有' + lis + '个商品')  # 有多少个li
print('最后一个商品是 ' + lis[-1].text + '个商品')  # 最后一个li
# 查看详情
# driver.find_element_by_xpath('//*[@id="result_0"]/div').click()
# 输出价格
# price = driver.find_element_by_id('priceblock_ourprice').text
# print('排名第一位的商品的售价为：' + price + '美元')

driver.quit()