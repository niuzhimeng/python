import urllib
from urllib.request import Request
from urllib.request import urlopen

from bs4 import BeautifulSoup

content = urllib.request.urlopen("http://tools.2345.com/carlist.htm")
# 伪装成浏览器访问
# req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
#                              ' Chrome/49.0.2623.112 Safari/537.36')

#content = urlopen(req).read().decode("gbk")

# soup = BeautifulSoup(content, 'html.parser')
soup = BeautifulSoup(content, 'lxml')
print(soup.prettify())
titles = soup.find_all('table')
#print(titles)
