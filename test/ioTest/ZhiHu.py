import time

import requests
from PIL import Image
from bs4 import BeautifulSoup

headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'
}

# 使用登录cookie信息
session = requests.session()


def get_xsrf():
    response = session.get("https://www.zhihu.com", headers=headers, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    xsrf = soup.find('input', attrs={"name": "_xsrf"}).get("value")
    return xsrf


def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    print(captcha_url)
    r = session.get(captcha_url, headers=headers)
    with open('nzm.jpg', 'wb') as f:
        f.write(r.content)
    im = Image.open('nzm.jpg')
    im.show()
    captcha = input("验证码：")
    return captcha


def login(email, password):
    login_url = 'https://www.zhihu.com/login/email'
    data = {
        'email': email,
        'password': password,
        '_xsrf': get_xsrf(),
        "captcha": get_captcha(),
        'remember_me': 'true'}
    response = session.post(login_url, data=data, headers=headers)
    login_code = response.json()
    print(login_code)
    r = session.get("https://www.zhihu.com", headers=headers)
    print(r.status_code)
    print(r.text)
    with open("D:/xx.html", "wb") as f:
        f.write(r.content)


if __name__ == '__main__':
    email = "295290968@qq.com"
    password = "nzm19940827"
    login(email, password)
