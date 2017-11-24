import execjs
import requests
import time

from PIL import Image

session = requests.session()
username = '295290968@qq.com'
password = 'nzm19940827'


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
    try:
        headers = {
            'Host': 'user.cwddd.com',
            'Connection': 'keep-alive',
            'Content-Length': '27',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'gzip, deflate'
        }
        url = 'http://user.cwddd.com/Public/checkUser.html'
        pwd = getPwd(password)
        session.post(url, headers=headers, data={'username': username, 'password': pwd})
        return True
    except Exception:
        return False


# 获取验证码
def get_yzm():
    yzm_h = {
        'User-Agent': 'xMozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Referer': 'http: //www.cwddd.com/Service/wfindex.html',
        'Host': 'hm3.cnzz.com',
        'X-Powered-By': 'PHP/5.2.17',
        'Vary': 'Accept-Encoding',
        'Server': 'nginx',
        'Pragma': 'no-cache'
    }
    t = str(int(time.time() * 1000))
    yzm_url = 'http://www.cwddd.com/Common/verify?ran=' + t
    yzm_res = session.get(yzm_url, headers=yzm_h)
    with open('cqyzm.jpg', 'wb') as f:
        f.write(yzm_res.content)
    im = Image.open('cqyzm.jpg')
    im.show()
    captcha = input('请输入验证码： ')
    return captcha


def get_verify_code(yzm):
    verify_code_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Origin': 'http://www.cwddd.com',
        'Referer': 'http://www.cwddd.com/',
        'Host': 'www.cwddd.com',
        'X-Requested-With': 'XMLHttpRequest'
    }
    verify_code_url = 'http://www.cwddd.com/Index/getSearchCosed'
    verify_code_res = session.post(verify_code_url, data={'verify': yzm}, headers=verify_code_header)
    verify_code = verify_code_res.text
    return verify_code


def check():
    check_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Origin': 'http://www.cwddd.com',
        'Referer': 'http://www.cwddd.com/',
        'Host': 'www.cwddd.com'
    }
    yzm = get_yzm()
    check_data = {
        'cartype': '02',
        'carnumber': '川A59ZT5',
        'verifyCode': get_verify_code(yzm),
        'carframe': '170943',
        'verify': yzm
    }

    u = 'http://hm3.cnzz.com/heatmap.gif?id=1253233115&x=1125&y=893&w=1349&s=1366x768&b=chrome&c=1&r=http%3A%2F%2Fwww.cwddd.com%2FService%2Factwf.html&a=0&p=http%3A%2F%2Fwww.cwddd.com%2F&random=Fri%20Nov%2024%202017%2017%3A57%3A44%20GMT%2B0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)'
    i = session.get(u).text
    print('=====' + i)
    check_url = 'http://www.cwddd.com/Service/actwf.html'
    check_res = session.post(check_url, data=check_data, headers=check_header)
    check_res.encoding = check_res.apparent_encoding
    print(check_res.text)


if __name__ == '__main__':
    if login():
        check()
