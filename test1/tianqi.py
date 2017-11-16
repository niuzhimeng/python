import re

import requests
from bs4 import BeautifulSoup

html = requests.get('http://www.tianqi.com/').text
page = BeautifulSoup(html, 'lxml')
div = page.find_all('div', id='i_airCont')
reg = re.compile(
    r'<li><em class="bg">(.*?)</em><b><a href=.*? target="_blank" title="">(.*?)</a></b><i>(.*?)</i><span style="color:#79b800">(.*?)</span></li>')
reg1 = re.compile(
    r'<li><em>(.*?)</em><b><a href=.*? target="_blank" title="">(.*?)</a></b><i>(.*?)</i><span style="color:#79b800">(.*?)</span></li>')
list = reg.findall(str(div))
list1 = reg1.findall(str(div))
list = list + list1
print('排名   ' + '城市   ' + '质量指数   ' + '质量状况    ')
for a, b, c, d in list:
    print(a + '     ' + b + '    ' + c + '      ' + d)
    
