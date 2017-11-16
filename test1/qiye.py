import re
import requests
from bs4 import BeautifulSoup

url = 'http://shuidi.cn/pc-search?key=' + '小米科技有限责任公司'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
html = requests.get(url, headers=headers).text
reg = re.compile(r'<a href="/company_info_(.*?).html')
num = reg.findall(html)
new_url = 'http://shuidi.cn/company_archives_' + str(num[0]) + '.html'

new_html = requests.get(new_url, headers=headers).text
soup = BeautifulSoup(new_html, 'lxml')
div_list = soup.find('div', class_='detail-info')

s = BeautifulSoup(str(div_list), 'lxml')
d = s.find_all('td')
new_5 = ''
for i, td in enumerate(d):
    if i % 2 == 0:
        print(td.get_text() + ': ', end='')
    elif i == 5:
        print(re.split(r'\s+?', td.get_text())[0])
    else:
        print(td.get_text())
