import random
import re

import requests

url = 'http://www.ip.cn/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}
pro = ['108.61.252.243:808', '186.46.156.202:65309', '165.244.150.199:80', '185.89.217.3:56560', '59.34.207.48:808',
       '122.5.132.137:44872']


# proxies = get_proxy()
# print(proxies)
def check(p):
    try:
        response = requests.get(url, proxies={'http': p})
    except Exception:
        return 'error'
    response.encoding = response.apparent_encoding
    code = response.status_code
    print(code)
    list = re.findall('<p>您现在的 IP：<code>(.*?)</code></p><p>(.*?)<code>(.*?)</code></p>', response.text)
    if 200 != code or len(list) == 0:
        return 'error'
    return list


if __name__ == '__main__':
    res = check(random.choice(pro))
    while 'error'.__eq__(str(res)):
        ip = random.choice(pro)
        print('当前访问ip：' + ip + ' 不好使')
        res = check(ip)
    print(res)
