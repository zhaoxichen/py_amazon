import os
import re
import urllib

import requests
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
    my_asin = 'B07964CWVK'
    keywords = 'dogs'
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
    # print(etree.tostring(html))
    print('-----------------------------------------------------------------------------------------')
    # //*[@id="s-results-list-atf"]
    print('***************' + keywords + '***************')
    ranking = 0
    while 1:
        result_titles = html.xpath(f'//*[@id="result_{ranking}"]/@data-asin')
        if 0 == len(result_titles):
            break
        asin_code = result_titles[0]
        print(f'result_{ranking}>>>' + asin_code)
        if my_asin == asin_code:
            print('我的商品排在>>>' + str(ranking))
            break
        ranking = ranking + 1
