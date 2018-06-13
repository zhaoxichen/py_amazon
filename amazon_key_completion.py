import requests
import re

unicornHeader = {
    'Host': 'www.amazon.com',
    'Referer': 'https://www.amazon.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

if __name__ == "__main__":
    # 第一步：先把amazon主页拉下来
    resp = requests.get("https://www.amazon.com/ref=nav_logo", headers=unicornHeader)
    respText = resp.text
    # print(f"respText = {respText}")

    # 第二步：从主页中提取出相关的参数
    '''
        method:completion
        mkt:1
        r:T9GNBFENMKCSHQ96SN69
        s:136-4489048-3064812
        c:
        p:Gateway
        l:en_US
        b2b:0
        fresh:0
        sv:desktop
        client:amazon-search-ui
        x:String
        search-alias:mobile
        ks:82
        q:car
        qs:
        cf:1
        fb:1
        sc:1
    '''
    # r:T9GNBFENMKCSHQ96SN69
    # var ue_id = 'T9GNBFENMKCSHQ96SN69',
    ue_id_Re = re.search("ue_id = '(.*?)'", respText, re.DOTALL)
    print(f"ue_id_Re = {ue_id_Re}")
    if ue_id_Re:
        ue_id = ue_id_Re.group(1)
    else:
        ue_id = ""

    # s:136-4489048-3064812
    # ue_sid = '136-4489048-3064812',
    ue_sid_Re = re.search("ue_sid = '(.*?)'", respText, re.DOTALL)
    print(f"ue_sid_Re = {ue_sid_Re}")
    if ue_sid_Re:
        ue_sid = ue_sid_Re.group(1)
    else:
        ue_sid = ""

    # 第三步：构造请求
    # 原始关键字
    originalKey = input('请输入要查询的原始关键词（回车）：')
    # search_alias = 'mobile'
    # aps                       # All Departments 类别
    search_alias = 'aps'  # 搜索类别，这个是类别下拉框中的。主页源码中也有
    ks = 100  # 先自己指定，发现并不影响结果
    # https://completion.amazon.com/search/complete?method=completion&mkt=1&r=T9GNBFENMKCSHQ96SN69&s=136-4489048-3064812&c=&p=Gateway&l=en_US&b2b=0&fresh=0&sv=desktop&client=amazon-search-ui&x=String&search-alias=mobile&ks=67&q=c&qs=&cf=1&fb=1&sc=1&
    keywordsUrl = f"https://completion.amazon.com/search/complete?method=completion&mkt=1&r={ue_id}&s={ue_sid}&c=&p=Gateway&l=en_US&b2b=0&fresh=0&sv=desktop&client=amazon-search-ui&x=String&search-alias={search_alias}&ks={ks}&q={originalKey}&qs=&cf=1&fb=1&sc=1&"
    secondResp = requests.get(keywordsUrl, headers=unicornHeader)
    print('*****************************************************************************************')
    print('原始关键词>>>' + originalKey)
    print('******************************按热度补全后的关键词列表如下****************************************')
    print(secondResp.text)
