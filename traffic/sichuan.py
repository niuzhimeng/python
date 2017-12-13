import re
import time

import execjs
import requests
from flask import Flask

app = Flask(__name__)
session = requests.session()
username = '295290968@qq.com'
password = 'nzm19940827'

if_login = 0


# 密码加密
def getPwd(pwd):
    url = 'http://user.cwddd.com/Public/getCode1'

    headers = {
        'Host': 'user.cwddd.com',
        'Connection': 'keep-alive',
        'Content-Length': '27',
        'Accept': '*/*',
        'Origin': 'http://user.cwddd.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://user.cwddd.com/Public/login',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    ssh_code = session.post(url, headers=headers, data={'username': username}).text
    jsstr = get_js()
    ctx = execjs.compile(jsstr)
    result = ctx.call("encode", ssh_code, pwd)
    return result


# 加载js
def get_js():
    f = open(r'C:\Users\txsk\Desktop\python\traffic/encode.js', 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr


def login():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Content-Length': '65',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'user.cwddd.com',
        'Origin': 'http://user.cwddd.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://user.cwddd.com/Public/login',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',

    }
    url = 'http://user.cwddd.com/Public/checkUser.html'
    pwd = getPwd(password)
    data = {
        'username': username,
        'password': pwd
    }
    # ,allow_redirects=False
    fi = session.post(url, headers=headers, data=data, allow_redirects=False)
    location = fi.headers['Location']
    s_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Referer': 'http://user.cwddd.com/Public/login',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive',
        'Host': 'www.cwddd.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    second = session.get(location, headers=s_header)
    second.text
    global if_login
    if_login = 1
    return '登录成功'


@app.route("/check_traffic_si_chuan", methods=['get'])
def sichuan():
    if if_login == 0:
        return login()
    else:
        return check()


# 获取验证码
def get_yzm():
    yzm_h = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Host': 'www.cwddd.com',
        'Referer': 'http://www.cwddd.com/'
    }
    # t = str(int(time.time() * 1000))
    # yzm_url = 'http://www.cwddd.com/Common/verify?ran=' + t
    yzm_url = 'http://www.cwddd.com/Common/verify'
    yzm_res = session.get(yzm_url, headers=yzm_h)
    with open('yzm.jpg', 'wb') as f:
        f.write(yzm_res.content)
    captcha = input('请输入验证码： ')
    return captcha


def get_verify_code(yzm):
    verify_code_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://www.cwddd.com/Service/wfindex.html',
        'Origin': 'http://www.cwddd.com',
        'Connection': 'keep-alive',
        'Host': 'www.cwddd.com'
    }
    verify_code_url = 'http://www.cwddd.com/Index/getSearchCosed'
    verify_code_res = session.post(verify_code_url, data={'verify': yzm}, headers=verify_code_header)
    verify_code = verify_code_res.text
    return verify_code


def check():
    check_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Origin': 'http://www.cwddd.com',
        'Referer': 'http://www.cwddd.com/Service/wfindex.html',
        'Host': 'www.cwddd.com',

        'Accept': 'image/webp,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive'
    }
    yzm = get_yzm()
    check_data = {
        'cartype': '02',
        'carnumber': '川A59ZT5',
        'verifyCode': get_verify_code(yzm),
        'carframe': '170943',
        'verify': yzm
    }

    check_url = 'http://www.cwddd.com/Service/actwf.html'
    check_res = session.post(check_url, data=check_data, headers=check_header)
    res = re.compile(r'<span class="no_VIP_icon fl"></span>\s*?<p>(.*?)</p>')
    print(check_res.text)
    mes = res.findall(check_res.text)
    return str(mes)


if __name__ == '__main__':
    app.run(host='192.168.3.213', port=8090, debug=False)