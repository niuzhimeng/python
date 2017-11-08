import requests
from bs4 import BeautifulSoup

page = requests.session().get('http://www.budejie.com/text/13', headers={'User-Agent':
                                                              'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'})

pageInfo = BeautifulSoup(page.text, 'html.parser')

div = pageInfo.find_all('div', 'j-r-list-c-desc')

for b in div:
    print(str(b.a) + '\r\n')
