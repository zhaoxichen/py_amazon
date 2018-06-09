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

    def get_product_position_title(self, key):
        global is_find
        write_str = ''
        # 查看商品标题
        product_list_title = driver.find_elements_by_xpath('//*[@id="s-results-list-atf"]/li/div/div//div[1]/a/h2')
        print(len(product_list_title))
        write_str += '这一页有' + str(len(product_list_title)) + '个商品\n\r'
        count_orders = 0
        for title_h2 in product_list_title:
            count_orders += 1
            title = title_h2.get_attribute('data-attribute')
            if self.my_title == title:
                print(key + '搜索我的商品，可以排在第' + str(count_orders) + '位')
                write_str += key + '搜索我的商品，可以排在第' + str(count_orders) + '位\n\r'
                write_str += title + '\n\r'
                is_find = 1
                break
        return write_str

    def product_search(self, key):
        driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]').clear()
        driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]').send_keys(key)
        driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input').click()

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

    # 写文件
    def write_file(self, file_path_out, str):
        if os.path.exists(self.work_space + file_path_out):
            file_path_keywords = self.work_space + file_path_out
            print('使用用户自定义' + file_path_keywords)
        elif os.path.exists(file_path_out):
            print('使用默认' + file_path_out)
        else:
            os.system(r"touch {}".format(file_path_out))  # 调用系统命令行来创建文件
        string = ''
        with open(file_path_out, "r+", encoding='utf-8') as rf:
            try:
                # 读每行
                list_of_all_the_lines = rf.readlines()
                for one_line in list_of_all_the_lines:
                    string += one_line
                rf.close()
                # 写
                wf = open(file_path_out, 'w+', encoding='utf-8')  # wf的 w+打开是删除txt内容，写入rf中修改的内容
                wf.write(string + str)
                wf.close()
            finally:
                rf.close()
                wf.close()


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://www.amazon.com')
    my_amazon = Amazon()
    # 点击下一页
    # driver.find_element_by_id('pagnNextString')
    keys_str = my_amazon.read_file('keywords.txt')
    key_arr = re.split('[,]', keys_str)
    counter = 0
    is_find = 0
    write_str = ''
    for my_key in key_arr:
        my_amazon.product_search(my_key)
        # 输入，搜索
        print('输入关键字   ' + my_key + '  搜索...')
        write_str += '输入关键字   ' + my_key + '  搜索...\n\r'
        write_str += my_amazon.get_product_position_title(my_key)
        # 点击下一页
        while 0 == is_find:
            counter += 1
            print("第" + str(counter) + '页')
            write_str += "第" + str(counter) + '页\n\r'
            if counter > 10:
                break
            write_str += my_amazon.get_product_position_title(my_key)
            try:
                next_page = driver.find_element_by_id('pagnNextString')
                next_page.click()
            except:
                print('异常了,没有下一页了')
                break
        time.sleep(1)
    # 写文件
    my_amazon.write_file("log.txt", write_str)
    driver.quit()
