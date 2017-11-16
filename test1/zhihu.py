import re
import time

import requests
from PIL import Image

headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'
}

session = requests.session()


def getXSRF():
    # 获取知乎首页的内容
    html = session.get("https://www.zhihu.com", headers=headers)
    p = re.compile('.*?<input type="hidden" name="_xsrf" value="(.*?)"/>.*?')
    html.encoding = html.apparent_encoding
    match = p.findall(html.text)
    xsrf = match[0]
    return xsrf


def get_yan_zheng():
    yanzhen_url = 'https://www.zhihu.com/captcha.gif?r=' + str(int(time.time() * 1000)) + "&type=login"
    haha = session.get(yanzhen_url, headers=headers)

    with open('code.jpg', 'wb') as f:
        f.write(haha.content)
    im = Image.open('code.jpg')
    im.show()
    yan = input('请输入验证码: ')
    return yan


# 登录的主方法
def login(email, password):
    login_url = 'https://www.zhihu.com/login/email'
    # post需要的表单数据，类型为字典
    login_data = {
        '_xsrf': getXSRF(),
        'password': password,
        'remember_me': 'true',
        'captcha': get_yan_zheng(),
        'email': email,
    }

    # 登录的URL
    # requests 的session登录，以post方式，参数分别为url、headers、data
    content = session.post(login_url, headers=headers, data=login_data)
    result_json = content.json()
    # 如果登录成功
    if 0 == result_json['r']:
        # 再次使用session以get去访问知乎首页，一定要设置verify = False，否则会访问失败
        s = session.get("http://www.zhihu.com", headers=headers, verify=False)
        print(s.text)
    else:
        print('登录失败')


if __name__ == "__main__":
    login("295290968@qq.com", "nzm19940827")
