import uuid

import pymysql
import requests
from bs4 import BeautifulSoup

url = 'http://tools.2345.com/carlist.htm'

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                        ' Chrome/49.0.2623.112 Safari/537.36'}

html = requests.get(url, headers=header)
soup = BeautifulSoup(html.text, 'lxml')

soup_one = soup.find_all('tr')

connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='nzm19940827',
                             db='amdb',
                             charset='utf8')
word = {}
for one in soup_one:
    tr = one.find_all(['td'])
    if tr:
        for index in range(len(tr) - 1):
            if tr[index].get('colspan') is None and tr[index] is not None:
                t = tr[index].get_text().strip()
                t1 = tr[index + 1].get_text().strip()
                if index % 2 == 0:
                    if t.strip() or t1.strip():
                        word[t] = t1
for a, b in word.items():
    if str(b).__contains__('市'):
        word[a] = b[:-1]

for c, d in word.items():
    print(c + '; ' + d)
try:
    # 获得数据库游标
    with connection.cursor() as cursor:
        sql = 'insert into pytest(id,province, number) values(%s,%s, %s)'
        for k, v in word.items():
            # 执行sql语句

            cursor.execute(sql, (int(uuid.uuid1()), k, v))
    # 事务提交
    connection.commit()
finally:
    # 关闭数据库连接
    connection.close()
