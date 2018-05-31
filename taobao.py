# coding=utf-8
'''
Created on 2016-8-16
@author: Jennifer
Project:使用chrome浏览器，安装chromewebdriver.exe
'''

from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://www.taobao.com')
# 输入，搜索
print('输入关键字   蓝牙  ,搜索...')
driver.find_element_by_xpath('//*[@id="q"]').send_keys('蓝牙')
driver.find_element_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button').click()
products_a_list = driver.find_elements_by_xpath('//*[@id="mainsrp-itemlist"]/div/div/div//div//div[1]/div/div[1]/a')
print(len(products_a_list))
for a in products_a_list:
    a.click()
    print(a.get_attribute('href'))
# print(len(products_url_list))

# 查看详情
# driver.find_element_by_xpath('//*[@id="result_0"]/div').click()
# 输出价格
# price = driver.find_element_by_id('priceblock_ourprice').text
# print('排名第一位的商品的售价为：' + price + '美元')

driver.quit()