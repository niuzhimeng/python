import re
import time

import requests
from PIL import Image
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from pytesseract import pytesseract

app = Flask(__name__)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Referer': 'http://www.njjg.gov.cn:81/simplequery/simplequery.aspx',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Host': 'www.njjg.gov.cn:81',
    'Origin': 'http://www.njjg.gov.cn:81',
    'Upgrade-Insecure-Requests': '1'}

session = requests.session()
res = session.post('http://www.njjg.gov.cn:81/simplequery/simplequery.aspx', headers=headers)


def check(post_data):
    response = session.post('http://www.njjg.gov.cn:81/simplequery/simplequery.aspx', headers=headers, data=post_data)
    if 200 != response.status_code:
        print('访问失败，错误码：  ' + response.status_code)
    return response.text


# 获取验证码，手动输入
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'http://www.njjg.gov.cn:81/GetValidate.aspx?n=4&t=' + t
    r = session.get(captcha_url, headers=headers)

    cook = r.cookies.get('validate_code')
    # print(cook)
    # with open('code.jpg', 'wb') as f:
    #     f.write(r.content)
    # im = Image.open('code.jpg')
    # vcode = pytesseract.image_to_string(im)
    # im.show()
    # print('识别的验证码：============ ' + vcode)
    # captcha = input("验证码：")
    #print(vcode)
    return cook


def get_viewstate():
    soup = BeautifulSoup(res.text, 'lxml')
    a = soup.find('input', id='__VIEWSTATE')
    b = a['value']
    return b


def get_EVENTVALIDATION():
    soup = BeautifulSoup(res.text, 'lxml')
    a = soup.find('input', id='__EVENTVALIDATION')
    b = a['value']
    return b


@app.route("/check_traffic", methods=['get'])
def check_traffic():
    license = request.args.get('license')
    carDriveNumber = request.args.get('carDriveNumber')
    post_data = {'lsb_PlateNo': '02',
                 'txt_BDate': '2015-11-15',
                 'txt_hp1': license[:2],
                 'txt_hp2': license[2:],
                 'txt_EDate': '2017-11-15',
                 'txt_fdjh': carDriveNumber,
                 'txtCheck': get_captcha(),
                 'btn_Query': '查 询',
                 '__VIEWSTATE': get_viewstate(),
                 '__EVENTVALIDATION': get_EVENTVALIDATION()}

    html = check(post_data)
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', attrs={'cellspacing': '0', 'rules': 'all'})
    if table is None:
        err = re.compile(r'<script>alert\(\'(.*?)\'\)</script>')
        return err.findall(html)[0]

    value = []
    result = []
    for t in BeautifulSoup(str(table), 'lxml').find_all('tr')[1:]:
        for d in t.find_all('td'):
            value.append(d.get_text())
    k = 0
    for i in range(int(len(value) / 6)):
        dic = {'id': value[k], 'monitoring_number': value[k + 1], 'time': value[k + 2], 'place': value[k + 3],
               'action': value[k + 4],
               'money': value[k + 5]}
        k += 6
        result.append(dic)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='192.168.3.213', port=8090, debug=False)
