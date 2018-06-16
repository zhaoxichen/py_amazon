import os
import re
import time
import urllib
from xlutils.copy import copy

import requests
import xlrd
import xlsxwriter
from lxml import etree

unicornHeader = {
    'Host': 'www.amazon.com',
    'Referer': 'https://www.amazon.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


# 读文件
def read_file(file_name):
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


if __name__ == "__main__":
    # 创建一个Excel文件
    today = time.strftime('%Y%m%d%H%M', time.localtime())
    file_name = '../excel/counter_' + today + '.xls'
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
    first = ['关键词', '搜索量']
    for i in range(0, len(first)):
        worksheet.write(0, i, first[i])
    workbook.close()  # 关闭
    row = 1
    while 1:
        search_count = []
        rexcel = xlrd.open_workbook(file_name)  # 用wlrd提供的方法读取一个excel文件
        rows = rexcel.sheets()[0].nrows  # 用wlrd提供的方法获得现在已有的行数
        excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
        table = excel.get_sheet(0)  # 用xlwt对象的方法获得要操作的sheet
        keywords_arr = []
        keywords_in = input('请输入关键词：')
        if '2' == keywords_in:
            keywords_in = read_file('../res_input/keyword_counter.txt')
            keywords_arr = re.split('[,]', keywords_in)
        elif '' == keywords_in:
            keywords_arr.append('cat')
        elif '88' == keywords_in:
            print('谢谢使用')
            break
        else:
            keywords_arr.append(keywords_in)
        print(keywords_arr)
        for keywords in keywords_arr:
            urldata = {
                'rh': 'i:aps,k:' + keywords,
                'field-keywords': keywords
            }
            urldata = urllib.parse.urlencode(urldata)
            url = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&" + urldata
            # 第一步 取出页面的数据
            resp = requests.get(url=url, headers=unicornHeader, stream=True)
            respContent = resp.content
            # print(f"respText = {respText}")

            # 第二步：从主页中提取出相关的参数
            # xpath解析需要的东西
            html = etree.HTML(respContent)
            result_counts = html.xpath('//*[@id="s-result-count"]')
            print(keywords + '>>>>搜索量>>>>>', end="")  # 使输出不换行
            if 0 < len(result_counts):
                result_count = result_counts[0]
                search_count.append(result_count.text)
                print(result_count.text)
            else:
                print('无')
                search_count.append('无')
        # 向excel写入数据
        for j in range(0, len(search_count)):
            table.write(row, 0, keywords_arr[j])
            table.write(row, 1, search_count[j])
            row = row + 1
        # 保存数据
        try:
            excel.save(file_name)
        except:
            print('***************************************数据写入失败***************************************')
            print('数据写入失败，请不要打开当前excel文件，请关闭当前正在操作的excel后，输入数字1，回车重试一次')
            print('***************************************数据写入失败***************************************')
            input('按回车重试一次:')
            try:
                excel.save(file_name)
            except:
                print('数据写入失败，抱歉！')
