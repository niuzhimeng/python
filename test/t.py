import requests
from bs4 import BeautifulSoup

phone = input('请输入手机号码： ')
url = 'http://www.ip138.com:8080/search.asp?mobile=' + phone + '&action=mobile'
page = requests.session().get(url)
page.encoding = 'gbk'
info = BeautifulSoup(page.text, 'lxml')
# print(info.prettify())
pageInfo = info.find_all('td', attrs={'align': 'center'})
i = 2
for info in pageInfo[1:]:
    if i % 2 == 0:
        if len(info.text) > 10:
            print(info.text.split(' ')[0] + '：', end=' ')
        else:
            print(info.text + '：', end=' ')
    else:
        if len(info.text) > 10:
            print(info.text.split(' ')[0])
        else:
            print(info.text)
    i += 1
