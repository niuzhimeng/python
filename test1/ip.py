import re

import requests
from bs4 import BeautifulSoup


def getData():
    arr = range(1, 342)  # 341ҳ
    sum = 0
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
    for i in arr:
        url = 'http://www.goubanjia.com/free/index' + str(i) + '.shtml'
        res = requests.get(url, headers=header)
        soup = BeautifulSoup(res.content, 'html.parser')
        ips = soup.find_all("td", attrs={"class": "ip"})
        with open('src/proxy', 'a') as file:
            sum += len(ips)
            for ip in ips:
                soup_ip = BeautifulSoup(str(ip), 'lxml')
                tag = soup_ip.td
                for j in tag.contents:
                    strs = ''
                    flag = re.search('none', str(j))
                    if flag is None:
                        if j.string is not None:
                            # print(tag.contents[j].string)
                            strs += j.string.strip()
                            # print(strs, end='')
                            if re.search('port', str(j)) is not None:
                                strs += '\n'
                    file.write(strs)
    print(sum)


if __name__ == '__main__':
    getData()
