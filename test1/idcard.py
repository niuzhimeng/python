import requests
from bs4 import BeautifulSoup

id_card = '230206199408270913'
url = 'http://qq.ip138.com/idsearch/index.asp?action=idcard&userid=' + id_card + '+&B1=%B2%E9+%D1%AF'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
html = requests.get(url, headers=header)
# html.encoding = 'gbk'
html.encoding = html.apparent_encoding
soup = BeautifulSoup(html.text, 'lxml')
list = soup.find_all('td', class_='tdc2')
for s in list:
    print(s.get_text())
