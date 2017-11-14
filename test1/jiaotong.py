import requests
import time

from PIL import Image

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}


def check():
    pass


# 获取验证码，手动输入
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'https://bj.122.gov.cn/captcha?nocache=' + t
    print(captcha_url)
    r = requests.get(captcha_url, headers=headers)
    with open('code.jpg', 'wb') as f:
        f.write(r.content)
    im = Image.open('code.jpg')
    im.show()
    captcha = input("验证码：")
    return captcha


if __name__ == '__main__':
    get_captcha()
