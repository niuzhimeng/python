import requests
from bs4 import BeautifulSoup

url = 'http://tools.2345.com/carlist.htm'

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/49.0.2623.112 Safari/537.36'}

html = requests.get(url, headers=header)
soup = BeautifulSoup(html.text, 'lxml')

soup_one = soup.find_all('tr')
word = []
for one in soup_one:
    tr = one.find_all(['td'])
    if tr:
        for td in tr:

            word.append(td)
for s in word:
    print(s)
