# coding=utf-8
'''
Created on 2016-8-16
@author: Jennifer
Project:使用chrome浏览器，安装chromewebdriver.exe
'''

import time
from threading import Timer

from selenium import webdriver


def loop_count_for_product_list():
    global order_count
    print('第' + str(order_count) + '次执行了')
    order_count += 1
    if order_count < 10:
        Timer(3, loop_count_for_product_list).start()


# 定时，重复执行
order_count = 0
print('开始监控：', time.time())
Timer(3, loop_count_for_product_list).start()
