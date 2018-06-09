# coding=utf-8
'''
Created on 2016-8-16
@author: Jennifer
Project:使用chrome浏览器，安装chromewebdriver.exe
'''
import time
import re
from selenium import webdriver


def get_product_position(key):
    # 查看商品封面图列表
    product_list_image = driver.find_elements_by_xpath('//*[@id="s-results-list-atf"]/li/div/div[2]/div/a/img')
    my_image = 'https://images-na.ssl-images-amazon.com/images/I/61rPa375ygL._AC_US200_.jpg'
    # my_image = 'https://images-na.ssl-images-amazon.com/images/I/61rPa375ygL._AC_US160_.jpg'
    count_orders = 0
    for image in product_list_image:
        count_orders += 1
        pic = image.get_attribute('src')
        if my_image == pic:
            print(key + '搜索我的商品，可以排在第' + str(count_orders) + '位')
            print(pic)
            break


def get_product_position_title(key):
    global is_find
    # 查看商品标题
    product_list_title = driver.find_elements_by_xpath('//*[@id="s-results-list-atf"]/li/div/div//div[1]/a/h2')
    print(len(product_list_title))
    # my_title = 'Newweic 4 Packs Rabbit Mats,Cage Plastic Spliced Feet Pads Water Leak Holders with Heart Hole for Bunny Rabbits Cat Cage Water Leak (Multi-colors)'
    my_title = '125ml Pet Drinking Bottle with Food Container Base Hanging Water Feeding Bottles Auto Dispenser for Hamsters Rats Small Animals Ferrets Rabbits Small Animals (125ML, Blue)'
    # my_image = 'https://images-na.ssl-images-amazon.com/images/I/61rPa375ygL._AC_US160_.jpg'
    count_orders = 0
    for title_h2 in product_list_title:
        count_orders += 1
        title = title_h2.get_attribute('data-attribute')
        if my_title == title:
            print(key + '搜索我的商品，可以排在第' + str(count_orders) + '位')
            print(title)
            is_find = 1
            break


driver = webdriver.Chrome()
driver.get('https://www.amazon.com')


def product_search(key):
    # 输入，搜索
    print('输入关键字   ' + key + '  搜索...')
    driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]').clear()
    driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]').send_keys(key)
    driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input').click()


# 点击下一页
# driver.find_element_by_id('pagnNextString')
keys_str ='hamster water bottle,hamster water bottle with base,hamster water bottle holder and bottle,water bottle for small animals,hamster water bottle,no drip water bottle for small animals,hamster water bottle with holder,hamster water bottle and food bowl,hamster food bowl,pet water dispenser bottle,pet water dispenser cage,small animal plastic water bottle '
key_arr = re.split('[,]', keys_str)
counter = 0
is_find = 0
for my_key in key_arr:
    product_search(my_key)
    # get_product_position(my_key)
    get_product_position_title(my_key)
    # 点击下一页
    while 0 == is_find:
        counter += 1
        print("第" + str(counter) + '页')
        if counter > 10:
            break
        get_product_position_title(my_key)
        try:
            next_page = driver.find_element_by_id('pagnNextString')
            next_page.click()
        except:
            print('异常了,没有下一页了')
            break
    time.sleep(1)
driver.quit()
