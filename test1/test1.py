
from urllib import request

from bs4 import BeautifulSoup

url = 'http://www.budejie.com/text/1'

result = request.Request(url)
result.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')
page = request.urlopen(result).read().decode('utf-8')
pageInfo = BeautifulSoup(page, 'lxml')
div = pageInfo.find_all('div', 'j-r-list-c-desc')

for b in div:
    print(str(b.a) + '\r\n')
