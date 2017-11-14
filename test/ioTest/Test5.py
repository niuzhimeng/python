import requests
import re

url = 'http://www.doutula.com/photo/list/?page=1 '

html = requests.get(url)
reg = r'data-original="(.*?)".*?alt="(.*?)"'
img_list = re.findall(reg, html.text, re.S)
for h, n in img_list:
    print(h + ' ' + n)
