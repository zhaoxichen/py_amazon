# coding=utf-8
'''
Created on 2016-8-16
@author: Jennifer
Project:使用chrome浏览器，安装chromewebdriver.exe
'''
import time
import re
import os
from selenium import webdriver


class Amazon():

    def __init__(self):
        # 工作空间
        self.work_space = 'D:\\Users\\'
        # 商品标题
        self.my_title = '125ml Pet Drinking Bottle with Food Container Base Hanging Water Feeding Bottles Auto Dispenser for Hamsters Rats Small Animals Ferrets Rabbits Small Animals (125ML, Blue)'

    def change_self_title(self, title_in):
        self.my_title = title_in

    def get_product_position_title(self):
        global is_find
        # 查看商品标题
        product_list_title = driver.find_elements_by_xpath('//*[@id="s-results-list-atf"]/li/div/div//div[1]/a/h2')
        print('本页共有' + str(len(product_list_title)) + '个商品')
        count_orders = 0
        for title_h2 in product_list_title:
            count_orders += 1
            title = title_h2.get_attribute('data-attribute')
            if self.my_title == title:
                print('我的商品可以排在第' + str(count_orders) + '位>>>> ' + title)
                is_find = 1
                break

    def product_search(self, key):
        driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]').clear()
        driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]').send_keys(key)
        driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input').click()

    # 元素存在，且唯一
    def is_element_exist_unique(self, css_str):
        s = driver.find_elements_by_css_selector(css_selector=css_str)
        if len(s) == 0:
            print
            "元素未找到:%s" % css_str
            return False
        elif len(s) == 1:
            return True
        else:
            print
            "找到%s个元素：%s" % (len(s), css_str)
            return False

    # 元素存在
    def is_element_exist(self, css_str):
        try:
            driver.find_element_by_css_selector(css_str)
            return True
        except:
            return False

    # 读文件
    def read_file(self, file_path_keywords):
        if os.path.exists(self.work_space + file_path_keywords):
            file_path_keywords = self.work_space + file_path_keywords
            print('使用用户自定义' + file_path_keywords)
        elif os.path.exists(file_path_keywords):
            print('使用默认' + file_path_keywords)
        else:
            return
        string = ''
        with open(file_path_keywords, "r+", encoding='utf-8') as rf:
            try:
                # 读每行
                list_of_all_the_lines = rf.readlines()
                for one_line in list_of_all_the_lines:
                    string += one_line
                rf.close()
                return string
            finally:
                rf.close()


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://www.amazon.com')
    my_amazon = Amazon()
    tile_in = input('请输入要查询的商品标题，回车确认：')
    my_amazon.change_self_title(tile_in)
    print('说明：')
    print('输入数字1或直接输入要查询的关键字，进入单个查询模式')
    print('输入数字2，进入多个轮询；输入英文exit，退出脚本')
    print('输入数字3,进入更换查询对象，更改商品标题')
    print('输入英文exit，退出脚本')
    # 无限循环
    while 1:
        # 判断要做的事情
        print('******************************************************************************')
        arm_handle = input('请指示模式或直接输入要查询的keyword，回车确认：')
        key_arr = []
        if '1' == arm_handle:
            key_in = input('请输入要查询的关键字，回车确认:')
            key_arr.append(key_in)
            print(key_arr)
        elif '2' == arm_handle:
            keys_str = my_amazon.read_file('keywords.txt')
            key_arr = re.split('[,]', keys_str)
        elif '3' == arm_handle:
            tile_in = input('更换要查询的商品标题，请输入，回车确认：')
            my_amazon.change_self_title(tile_in)
        elif 'exit' == arm_handle:
            # 退出
            print('***************************************谢谢支持！！！***************************************')
            break
        else:
            # 默认是单个关键字查询模式
            key_arr.append(arm_handle)
            print(key_arr)

        for my_key in key_arr:
            # 输入，搜索
            print('输入关键字   ' + my_key + '  搜索...')
            my_amazon.product_search(my_key)
            # 搜索需要加载时间
            time.sleep(3)
            counter = 0
            is_find = 0
            # 开始查询
            while 0 == is_find:
                counter += 1
                print("第" + str(counter) + '页')
                # 获取位置
                my_amazon.get_product_position_title()
                if 1 == is_find:
                    break
                if counter > 10:
                    break
                if my_amazon.is_element_exist_unique('pagnNextString'):
                    next_page = driver.find_element_by_id('pagnNextString')
                    next_page.click()
                    # 翻页加载需要时间
                    time.sleep(3)
                else:
                    print('翻完了所有页码都没有找到,这都写的什么关键字呀！！！！')
                    break
        print('***************************************本次查询工作完成***************************************')
    # 关闭浏览器
    driver.quit()
    print('***************************************再见！！！***************************************')
