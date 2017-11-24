import re
import time

import requests
from PIL import Image
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)
session = requests.session()

change = {'A': '11', 'B': '12', 'C': '13', 'D': '14', 'E': '15', 'F': '16', 'G': '17', 'H': '18', 'J': '20', 'R': '28',
          'S': '29', 'T': '30', 'O': '25'}

check_url = 'http://www.hbgajg.com/service/show-12-42.html'

html = ''


def get_ssh_code(vin, car_number):
    check_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Host': 'www.hbgajg.com',
        'Origin': 'http://www.hbgajg.com',
        'Referer': 'http://www.hbgajg.com/'
    }
    check_body = {
        'CC_JDCWZ_OneArea': '11',
        'CC_JDCWZ_OneZimu': change.get(car_number[1:2]),
        'CC_JDCWZ_Two': car_number[2:],
        'CC_JDCWZ_Three': '02',
        'CC_JDCWZ_Four': vin,
        'aapi': 'a1'
    }
    check_res = session.post(check_url, data=check_body, headers=check_header)
    check_res.encoding = check_res.apparent_encoding
    global html
    html = check_res.text
    t = str(int(time.time() * 1000))
    ssh_url = re.findall(r'\$.getJSON\("(.*?)"\+new Date\(\)\.getTime\(\)', html)
    ssh_url = ssh_url[1] + t
    res = session.get(ssh_url)
    return res.text[13:-3]


def get_yzm(ssh_code):
    yzm_header = {
        'Accept': 'image/webp,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Host': 'apicode.hbgajg.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Referer': 'http://www.hbgajg.com/service/show-12-42.html',
    }
    yzm_url = 'http://apicode.hbgajg.com/api.php?op=acheckcode&code_len=2&fdjh=default_sg&wb=1&sshcode=' + ssh_code
    yzm_res = session.get(yzm_url, headers=yzm_header)
    print(yzm_res.content)
    if yzm_res.status_code != 200:
        print('验证码状态： ' + str(yzm_res))
        return '验证码获取异常'
    with open('yzm.jpg', 'wb') as f:
        f.write(yzm_res.content)
    im = Image.open('yzm.jpg')
    im.show()
    captcha = input('请输入验证码： ')
    return captcha


@app.route("/check_traffic_heBei", methods=['get'])
def check():
    vin = request.args.get('vin')
    car_number = request.args.get('carNumber')
    # 获取ssh_code码
    ssh_code = get_ssh_code(vin, car_number)
    # 获取验证码
    captcha = get_yzm(ssh_code)
    t = str(int(time.time() * 1000))
    yzm_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }
    ajax = 'http://apicode.hbgajg.com/testcode.php?hphm=' + \
           car_number[2:] + '&inputcode=' + captcha + '&sslcode=' + ssh_code + '&nocache=' + t
    aa = session.get(ajax, headers=yzm_header)
    print('校验验证码返回： ' + aa.text)
    if not aa.text.__contains__('1'):
        return '验证码错误'

    # 获取隐藏域内的信息
    _hphm = re.findall(r'<input type="hidden" name="_hphm" value="(.*?)" />', html)
    sbdm = re.findall(r'<input type="hidden" name="sbdm" value="(.*?)" />', html)
    pAutoID = re.findall(r'<input type="hidden" name="pAutoID" value="(.*?)" />', html)
    page = re.findall(r'<input type="hidden" name="page" value="(.*?)" />', html)
    ko = re.findall(r'<input type="hidden" name="ko" id="ko" value="(.*?)">', html)

    # 拼接请求体
    second_body = {
        'inputcode': captcha.encode('gbk'),  # 该网站是gbk编码
        'sshcode': ssh_code,
        '_hphm': _hphm[0],
        'sbdm': sbdm[0],
        'pAutoID': pAutoID[0],
        'page': page[0],
        'ko': ko[0]
    }
    ajax_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Referer': 'http://www.hbgajg.com/service/show-12-42.html',
        'Host': 'www.hbgajg.com',
        'Origin': 'http://www.hbgajg.com'
    }
    result = session.post(check_url, data=second_body, headers=ajax_header)
    result.encoding = result.apparent_encoding
    end_result = result.text

    totle = re.findall(r'<span>（总计：<b>(.*?)</b> 条违法记录,记 <b>(.*?)</b> 分,罚款 <b>(.*?)</b> 元）</span>', end_result)
    if len(totle) < 1:
        return '无违章信息'
    # 车身颜色等信息
    info = re.findall(
        r'<dt style="position:relative;z-index:99999;"><b>有效期至：</b><span>(.*?)</span>\s*?(.*?)\s*?</dt>\s*?<dt><b>车身颜色：</b>(.*?)</dt>\s*?<dt><b>车辆状态：</b>(.*?)</dt>',
        end_result, re.M)
    value = []
    result_map = {}
    if len(totle[0]) > 2:
        result_map = {'违章记录总数': totle[0][0], '总扣分': totle[0][1], '总罚款': totle[0][2]}
    if len(info[0]) > 3:
        result_map['有效期至'] = info[0][0] + info[0][1].strip()
        result_map['车辆颜色'] = info[0][2]
        result_map['车辆状态'] = info[0][3]

    result_value = []
    soup = BeautifulSoup(end_result, 'lxml')
    table_soup = soup.find_all('table', class_='tb_sr')
    td_soup = BeautifulSoup(str(table_soup), 'lxml').find_all('td')
    for td in td_soup:
        value.append(td.string.strip())

    k = 0
    for i in range(int(len(value) / 8)):
        dic = {
            '序号': value[k],
            '处理标记': value[k + 1],
            '记分分数': value[k + 2],
            '罚款金额': value[k + 3],
            '违法时间': value[k + 4],
            '采集机关': value[k + 5],
            '违法地址': value[k + 6],
            '违法行为': value[k + 7]
        }
        k += 8
        result_value.append(dic)
    result_map['data'] = result_value
    return jsonify(result_map)


if __name__ == '__main__':
    app.run(host='192.168.3.213', port=8090, debug=False)
