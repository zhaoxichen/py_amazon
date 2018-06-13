import urllib

import requests
import re
from lxml import etree

unicornHeader = {
    'Host': 'www.amazon.com',
    'Referer': 'https://www.amazon.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

if __name__ == "__main__":
    urldata = {
        'rh': 'i:aps,k:cat',
        'field-keywords': 'cat'
    }
    urldata = urllib.parse.urlencode(urldata)
    url = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&" + urldata
    # 第一步 取出页面的数据
    resp = requests.get(url=url, headers=unicornHeader, stream=True)
    respText = resp.text
    # print(f"respText = {respText}")

    # 第二步：从主页中提取出相关的参数
    '''
     <span id="s-result-count">1-48 of over 500,000 results for <span>
    '''
    # r:T9GNBFENMKCSHQ96SN69
    # var ue_id = 'T9GNBFENMKCSHQ96SN69',
    # 找到商品名称
    html = resp.content
    # xpath解析需要的东西
    contents = etree.HTML(html)
    result_counts = contents.xpath('//*[@id="s-result-count"]')
    for result_count in result_counts:
        print('****************************************************')
        print(result_count)

