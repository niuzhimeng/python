import base64
import time

import requests
from PIL import Image
from pytesseract import pytesseract

session = requests.session()
username = '295290968@qq.com'
password = 'nzm19940827'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Referer': 'http://www.cqjg.gov.cn/cxxt/jdcwf.html',
    'Host': 'www.cqjg.gov.cn',
    'Origin': 'http://www.cqjg.gov.cn/cxxt/jdcwf.html'}


# 获取验证码，手动输入
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'http://www.cwddd.com/Common/verify?ran=' + t
    r = session.get(captcha_url, headers=headers)
    with open('code.jpg', 'wb') as f:
        f.write(r.content)
    im = Image.open('code.jpg')
    vcode = pytesseract.image_to_string(im)
    # im.show()
    # print('识别的验证码：============ ' + vcode)
    # captcha = input("验证码：")
    return vcode


def check_traffic():
    response = session.post('http://www.cqjg.gov.cn/cxxt/jdccxjg.html', headers=headers, data=post_data)
    if 200 != response.status_code:
        print('访问失败，错误码：  ' + response.status_code)
    return response.text


def login(cookie):
    code = get_code()
    print(code)
    print(code[6])
    seven = input('输入上面字母下一位： ')
    pwd = code[0:6] + seven + 'uem0xOTk0MDgyNw=='
    print(pwd)
    login_data = {
        'username': username,
        'password': pwd
    }
    php = cookie['PHPSESSID']
    coo = 'PHPSESSID=' + php
    login_header = {
        'Host': 'user.cwddd.com',
        'Connection': 'keep - alive',
        'Cache - Control': 'max-age=0',
        'Origin': 'http://user.cwddd.com',
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Cookie': coo,
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Content-Length': '65',
        'Content - Length': '65',
        'Upgrade - Insecure - Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://www.cwddd.com/Service/actwf.html'
    }

    login_url = 'http://user.cwddd.com/Public/checkUser.html'
    log_res = session.post(login_url, data=login_data, headers=login_header)
    log_res.encoding = 'utf-8'
    print(log_res.text)


def get_code():
    code_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Origin': 'http://user.cwddd.com',
        'Referer': 'http://user.cwddd.com/Public/login',
        'Host': 'user.cwddd.com',
        'X-Requested-With': 'XMLHttpRequest'
    }
    code_data = {
        'username': username
    }
    get_code_url = 'http://user.cwddd.com/Public/getCode1'
    get_code_res = session.post(get_code_url, headers=code_header, data=code_data, cookies=get_cookid())
    return get_code_res.text


def get_cookid():
    code_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }
    cook_url = 'http://user.cwddd.com/Public/login'
    cook_res = session.post(cook_url, headers=code_header)
    return dict(cook_res.cookies)


if __name__ == '__main__':
    post_data = {'hpzl': '02',
                 'hphm': '渝AZL525',
                 'vin': '912520',
                 'yzm': ''}

    login(get_cookid())
    # check_traffic()
