import os
import re
import time
import urllib

import requests
import xlrd
import xlsxwriter
from xlutils.copy import copy
from lxml import etree


class Amazon():

    def __init__(self):
        # 商品标题
        self.my_title = '125ml Pet Drinking Bottle with Food Container Base Hanging Water Feeding Bottles Auto Dispenser for Hamsters Rats Small Animals Ferrets Rabbits Small Animals (125ML, Blue)'
        self.my_asin = 'B07964CWVK'
        self.out_file_name = '../excel/default.xls'
        self.unicornHeader = {
            'Host': 'www.amazon.com',
            'Referer': 'https://www.amazon.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }

    def change_self_asin(self, asin_in):
        self.my_asin = asin_in

    def get_product_position_title(self):
        global is_find
        # 查看商品标题
        product_list_title = ''
        print('本页共有' + str(len(product_list_title)) + '个商品，', end='')
        count_orders = 0
        for title_h2 in product_list_title:
            count_orders += 1
            title = title_h2.get_attribute('data-attribute')
            if self.my_title == title:
                print('我们的商品可以排在第' + str(count_orders) + '位>>>> ' + title)
                is_find = 1
                return count_orders

    # 读文件
    def read_file(self, file_name):
        if os.path.exists(file_name):
            print(file_name)
        else:
            file_dir = os.path.split(file_name)[0]
            # 判断文件路径是否存在，如果不存在，则创建，此处是创建多级目录
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
            file = open(file_name, 'w')
            file.close()
        string = ''
        with open(file_name, "r+", encoding='utf-8') as rf:
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
    def write_out_to_excel(self, arr_ad, arr_page, arr_pos, arr_total_pos, keyword):
        rexcel = xlrd.open_workbook(self.out_file_name)  # 用wlrd提供的方法读取一个excel文件
        rows = rexcel.sheets()[0].nrows  # 用wlrd提供的方法获得现在已有的行数
        excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
        table = excel.get_sheet(0)  # 用xlwt对象的方法获得要操作的sheet
        # 向excel写入数据
        rows = rows + 1
        for j in range(0, len(arr_page)):
            table.write(rows, 0, keyword)
            table.write(rows, 1, arr_page[j])
            table.write(rows, 2, arr_pos[j])
            table.write(rows, 3, arr_total_pos[j])
            table.write(rows, 5, self.my_asin)
            table.write(rows, 6, arr_ad[j])
            rows = rows + 1
        # 保存数据
        try:
            excel.save(self.out_file_name)
        except:
            print('***************************************数据写入失败***************************************')
            print('数据写入失败，请不要打开当前excel文件，请关闭当前正在操作的excel后，输入数字1，回车重试一次')
            print('***************************************数据写入失败***************************************')
            input('输入数字1，按回车重试一次:')
            try:
                excel.save(self.out_file_name)
            except:
                print('数据写入失败，抱歉！')

    def match_one_key(self, keyword):
        global is_find
        is_find = 0
        arr_keys_find = []
        arr_page = []
        arr_pos = []
        arr_total_pos = []
        arr_ad = []
        for page in range(1, 10):
            print('*******************************第' + str(page) + '页**************************************')
            urldata = {
                'rh': 'i:aps,k:' + keyword,
                'field-keywords': keyword,
                'page': page
            }
            urldata = urllib.parse.urlencode(urldata)
            url = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&" + urldata
            # 第一步 取出页面的数据
            resp = requests.get(url=url, headers=my_amazon.unicornHeader, stream=True)
            respContent = resp.content
            # 第二步：从主页中提取出相关的参数
            # xpath解析需要的东西
            html = etree.HTML(respContent)
            result_titles = html.xpath('//li[@data-asin]')
            total_product = len(result_titles)
            if 0 == total_product:
                print('没有下一页了')
                break
            print('这一页有' + str(total_product) + '个商品')
            ranking = 0
            for result_title in result_titles:
                result_id = result_title.get('id')
                result_asin_code = result_title.get('data-asin')
                result_class = result_title.get('class')
                if self.my_asin == result_asin_code:
                    print('我的商品排在>>>' + str(page) + '页' + str(ranking) + '位')
                    arr_keys_find.append(keyword)
                    arr_page.append(page)
                    arr_pos.append(ranking)
                    arr_total_pos.append(result_id)
                    if 'AdHolder' in result_class:
                        arr_ad.append('广告')
                    else:
                        arr_ad.append('自然排名')
                    is_find = 1  # 找到了
                    # break
                ranking = ranking + 1
        # 打开exce文件,可追加写入
        if 1 == is_find:
            self.write_out_to_excel(arr_ad, arr_page, arr_pos, arr_total_pos, keyword)


# 程序入口
if __name__ == "__main__":
    my_amazon = Amazon()
    asin_in = input('请输入要查询商品的ASIN码，回车确认：')
    if '2' == asin_in:
        my_asin_file = '../res_input/my_asin.txt'
        asin_in = my_amazon.read_file(my_asin_file)
    if '' == asin_in:
        print(my_amazon.my_asin)
    else:
        my_amazon.change_self_asin(asin_in)
    print('查询的商品>>>' + my_amazon.my_asin)
    print('说明：')
    print('输入数字1或直接输入要查询的关键字，进入单个查询模式')
    print('输入数字2，进入多个轮询')
    print('输入数字3,进入更换查询对象，更改商品标题')
    print('输入数字88，退出脚本')
    # 创建一个Excel文件
    today = time.strftime('%Y%m%d%H%M', time.localtime())
    file_name = f'../excel/{today }.xls'
    file_dir = os.path.split(file_name)[0]
    # 判断文件路径是否存在，如果不存在，则创建，此处是创建多级目录
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    # 然后再判断文件是否存在，如果不存在，则创建
    if not os.path.exists(file_name):
        file = open(file_name, 'w')
        file.close()
    # 创建一个Excel文件
    workbook = xlsxwriter.Workbook(file_name)
    # 创建一个工作表
    worksheet = workbook.add_worksheet()
    # 写入第标题行
    first = ['关键词', '页码', '当页排名', '总排名', '商品地址', '商品ASIN码', '是否广告']
    for i in range(0, len(first)):
        worksheet.write(0, i, first[i])
    workbook.close()  # 关闭
    my_amazon.out_file_name = file_name
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
            my_keys_file = '../res_input/keywords.txt'
            keys_str = my_amazon.read_file(my_keys_file)
            if '' == keys_str:
                print('文本中没有预设关键词')
            else:
                key_arr = re.split('[,]', keys_str)
        elif '3' == arm_handle:
            asin_in = input('更换要查询的ASIN，请输入，回车确认：')
            if '2' == asin_in:
                asin_in = my_amazon.read_file(my_asin_file)
            if '' == asin_in:
                print(my_amazon.my_asin)
            else:
                my_amazon.change_self_asin(asin_in)
            print('查询的商品>>>' + asin_in)
            continue
        elif '88' == arm_handle:
            # 退出
            print('***************************************谢谢支持！！！***************************************')
            break
        elif '' == arm_handle:
            key_arr.append('hamster water bottle with base')
        else:
            # 默认是单个关键字查询模式
            key_arr.append(arm_handle)
            print(key_arr)

        for my_key in key_arr:
            # 输入，搜索
            print('搜索>>>' + my_key)
            my_amazon.match_one_key(my_key)
            # 搜索需要加载时间
            time.sleep(3)
        print('***************************************本次查询工作完成***************************************')
    print('***************************************再见！！！***************************************')
