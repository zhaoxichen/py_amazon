import os
import re
import urllib

import requests
from lxml import etree

unicornHeader = {
    'Host': 'www.amazon.ca',
    'Referer': 'https://www.amazon.ca',
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
    while 1:
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
            print('***************' + keywords + '***************')
            if 0 < len(result_counts):
                result_count = result_counts[0]
                print(result_count.text)
