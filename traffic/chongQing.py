import time

import requests
from PIL import Image
from pytesseract import pytesseract

session = requests.session()

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


if __name__ == '__main__':
    post_data = {'hpzl': '02',
                 'hphm': '渝AZL525',
                 'vin': '912520',
                 'yzm':''}
    check_traffic()
