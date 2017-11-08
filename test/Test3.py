import requests
from bs4 import BeautifulSoup


# 从网络上获取大学排名网页的内容
def getHtmlText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return (r.text)
    except:
        return ('')


# 提取网页中的信息到合适数据结构
def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find_all(id='Tabs_zhb', class_='conBox zhb')
    # 寻找标签<div class="conBox zhb" id="Tabs_zhb">
    table = item[0].find_all('table')
    # 寻找上个标签下的<table>标签
    for item1 in table:
        tr = item1.find_all('tr')
        # 寻找<table>标签下的各个<tr>标签
        for item in tr[1:]:
            # 去掉第一个<tr>标签，从第二个开始遍历
            aim = item.contents
            # <tr>标签下的内容，也就是各个<td>标签
            if len(aim) > 10:
                ulist.append([aim[1].string,
                              aim[3].find_all('a')[0].string,
                              aim[9].string])


# 利用数据结构展示输出结构
def printUnivList(ulist, num):
    tplt = '{0:^10}\t{1:{3}^10}\t{2:^10}'
    # 输出的结构布置
    print(tplt.format('大学综合排名', '学校所在地', '总得分', chr(12288)))
    # chr(12288)是中文空格填充字符
    for i in range(num):
        u = ulist[i]
        print(tplt.format(u[0], u[1], u[2], chr(12288)))


def main():
    unifo = []
    url = 'http://www.eol.cn/html/ky/16phb/'
    html = getHtmlText(url)
    fillUnivList(unifo, html)
    printUnivList(unifo, 40)  # 只列出40所学校的信息


main()
