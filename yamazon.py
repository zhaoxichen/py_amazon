# coding=utf-8

import requests
import time
import random
import xlsxwriter
from lxml import etree
import urllib.parse
import urllib.request
import os


def geturl(url):
    # 制作头部
    header = {
        'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 4_3_4 like Mac OS X; ja-jp) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8K2 Safari/6533.18.5',
        'Referer': 'https://www.amazon.cn/',
        'Host': 'www.amazon.cn',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive'
    }
    # get参数
    res = requests.get(url=url, headers=header)
    # ('UTF-8')('unicode_escape')('gbk','ignore')
    resdata = res.content
    return resdata


def getimg(url):
    # 制作头部
    header = {
        'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 4_3_4 like Mac OS X; ja-jp) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8K2 Safari/6533.18.5',
        'Referer': 'https://www.amazon.cn/',
        'Host': 'www.amazon.cn',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive'
    }
    # get参数
    res = requests.get(url=url, headers=header, stream=True)
    # ('UTF-8')('unicode_escape')('gbk','ignore')
    resdata = res.iter_content(chunk_size=1024)
    for chunk in resdata:
        if chunk:
            return chunk


def begin():
    taoyanbai = '''
             -----------------------------------------
             | 欢迎使用亚马逊爬取系统                   |
             | 时间：2016年9月20日                   |
             | 出品：TTyb                           |
             | 微信/QQ：420439007                    |
             -----------------------------------------
         '''
    print(taoyanbai)


def timetochina(longtime, formats='{}天{}小时{}分钟{}秒'):
    day = 0
    hour = 0
    minutue = 0
    second = 0
    try:
        if longtime > 60:
            second = longtime % 60
            minutue = longtime // 60
        else:
            second = longtime
        if minutue > 60:
            hour = minutue // 60
            minutue = minutue % 60
        if hour > 24:
            day = hour // 24
            hour = hour % 24
        return formats.format(day, hour, minutue, second)
    except:
        raise Exception('时间非法')


if __name__ == '__main__':

    begin()
    keyword = input("请输入关键词：")
    try:
        sort = int(input("相关度排序请按0，人气排序请按1，上架时间排序请按2，价格低到高排序请按3，价格高到低请按4，用户评分排序请按5（默认相关度排序）："))
        if sort > 5 or sort <= 0:
            sort = ""
        elif sort == 1:
            sort = "popularity-rank"
        elif sort == 2:
            sort = "date-desc-rank"
        elif sort == 3:
            sort = "price-asc-rank"
        elif sort == 4:
            sort = "price-desc-rank"
        elif sort == 5:
            sort = "review-rank"
    except:
        sort = ""
    try:
        pages = int(input("请输入抓取页数（默认5页）："))
    except:
        pages = 5

    a = time.clock()

    # 转成字符串
    # %y 两位数的年份表示（00 - 99）
    # %Y 四位数的年份表示（000 - 9999）
    # %m 月份（01 - 12）
    # %d 月内中的一天（0 - 31）
    # %H 24小时制小时数（0 - 23）
    # %I 12小时制小时数（01 - 12）
    # %M 分钟数（00 = 59）
    # %S 秒（00 - 59）
    today = time.strftime('%Y%m%d%H%M', time.localtime())
    # 创建一个Excel文件
    workbook = xlsxwriter.Workbook('../excel/' + today + '.xlsx')
    # 创建一个工作表
    worksheet = workbook.add_worksheet()

    # 第一行参数
    first = ['商品名称', '品牌', '详情页网址', '原价格', '星级', '图片', '图片网址']

    # 写入excel计数行
    count = 1

    # 下载图片计数
    num = 0

    # 构造时间戳
    nowtime = int(time.time())

    for page in range(0, pages):

        urldata = {
            'page': page,
            'sort': sort,
            'keywords': keyword,
            'ie': 'UTF-8',
            'qid': str(nowtime)
        }
        urldata = urllib.parse.urlencode(urldata)
        url = "https://www.amazon.cn/s/ref=nb_sb_noss_1?__mk_zh_CN=亚马逊网站&" + urldata

        html = geturl(url).decode('Utf-8', 'ignore')

        # xpath解析需要的东西
        contents = etree.HTML(html)

        # 找到商品名称
        titles = contents.xpath('//a[@class="a-link-normal s-access-detail-page  a-text-normal"]/@title')
        arr_title = []
        for title in titles:
            arr_title.append(title)

        # 找到品牌
        brands = contents.xpath('//div[@class="a-row a-spacing-mini"][1]/div/span/text()')
        arr_brand = []
        for brand in brands:
            if "更多购买选择" in brand:
                pass
            else:
                arr_brand.append(brand)

        # 找到详情页网址
        detailurls = contents.xpath('//a[@class="a-link-normal s-access-detail-page  a-text-normal"]/@href')
        arr_detailurl = []
        for detailurl in detailurls:
            arr_detailurl.append(urllib.parse.unquote(detailurl))

        # 得到原价格
        # 这里是忽略了新品价格、非新品价格
        prices = contents.xpath('//div[@class="a-row a-spacing-none"][1]/a/span[1]/text()')
        arr_price = []
        for price in prices:
            arr_price.append(price)

        # 得到星级
        grades = contents.xpath('//span[@class="a-icon-alt"]/text()')
        arr_grade = []
        for grade in grades:
            if "平均" in grade:
                arr_grade.append(grade)
                # print(grade)
            else:
                pass
        if arr_grade:
            arr_grade.pop()
        # print(len(arr_grades))

        # 得到图片
        imgurls = contents.xpath('//a[@class="a-link-normal a-text-normal"]/img/@src')
        arr_img = []
        # 将文件路径分割出来
        file_name = "../jpg/" + str(num) + ".jpg"
        file_dir = os.path.split(file_name)[0]
        # 判断文件路径是否存在，如果不存在，则创建，此处是创建多级目录
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        # 然后再判断文件是否存在，如果不存在，则创建
        if not os.path.exists(file_name):
            os.system(r'touch %s' % file_name)
        for imgurl in imgurls:
            file = open("../jpg/" + str(num) + ".jpg", "wb")
            pic = urllib.request.urlopen(imgurl)
            file.write(pic.read())
            file.close()
            # 每一次下载都暂停1-3秒
            imgtime = random.randint(1, 3)
            print("下载图片暂停" + str(imgtime) + "秒")
            time.sleep(imgtime)
            arr_img.append(imgurl)
            num = num + 1
            # print(imgurl)
        # print(len(arr_img))

        # 写入excel
        # 写入第一行
        for i in range(0, len(first)):
            worksheet.write(0, i, first[i])

        # 写入其他数据
        for j in range(0, len(arr_title)):
            worksheet.write(count, 0, arr_title[j])
            worksheet.write(count, 1, arr_brand[j])
            worksheet.write(count, 2, arr_detailurl[j])
            try:
                worksheet.write(count, 3, arr_price[j])
            except Exception as err:
                print(err)
                worksheet.write(count, 3, "")
            worksheet.write(count, 4, arr_grade[j])
            worksheet.insert_image(count, 5, "../jpg/" + str(count - 1) + ".jpg")
            worksheet.write(count, 6, arr_img[j])
            count = count + 1

        # 每一次下载都暂停5-10秒
        loadtime = random.randint(5, 10)
        print("抓取网页暂停" + str(loadtime) + "秒")
        time.sleep(loadtime)

    workbook.close()
    b = time.clock()
    print('运行时间：' + timetochina(b - a))
    input('请关闭窗口')
