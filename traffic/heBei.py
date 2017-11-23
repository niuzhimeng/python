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


@app.route("/check_traffic_heBei", methods=['get'])
def check():
    vin = request.args.get('vin')
    carNumber = request.args.get('carNumber')

    check_url = 'http://www.hbgajg.com/service/show-12-42.html'
    check_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Host': 'www.hbgajg.com',
        'Origin': 'http://www.hbgajg.com',
        'Referer': 'http://www.hbgajg.com/'
    }
    check_body = {
        'CC_JDCWZ_OneArea': '11',
        'CC_JDCWZ_OneZimu': change.get(carNumber[1:2]),
        'CC_JDCWZ_Two': carNumber[2:],
        'CC_JDCWZ_Three': '02',
        'CC_JDCWZ_Four': vin,
        'aapi': 'a1'
    }
    check_res = session.post(check_url, data=check_body, headers=check_header)
    check_res.encoding = check_res.apparent_encoding
    html = check_res.text
    t = str(int(time.time() * 1000))
    ssh_url = re.findall(r'\$.getJSON\("(.*?)"\+new Date\(\)\.getTime\(\)', html)
    ssh_url = ssh_url[1] + t
    res = session.get(ssh_url, headers=check_header)
    ssh_code = res.text[13:-3]

    yzm_url = 'http://apicode.hbgajg.com/api.php?op=acheckcode&code_len=2&fdjh=default_sg&wb=1&sshcode=' + ssh_code
    yzm_res = session.get(yzm_url)
    with open('yzm.jpg', 'wb') as f:
        f.write(yzm_res.content)

    im = Image.open('yzm.jpg')
    im.show()
    captcha = input('请输入验证码： ')

    ajax_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Referer': 'http://www.hbgajg.com/service/show-12-42.html',
        'Host': 'apicode.hbgajg.com'
    }
    ajax = 'http://apicode.hbgajg.com/testcode.php?hphm=X0536&inputcode=' + captcha + '&sslcode=' + ssh_code + '&nocache=' + t
    aa = session.get(ajax, headers=ajax_header)
    if not aa.text.__contains__('1'):
        return '验证码错误'

    _hphm = re.findall(r'<input type="hidden" name="_hphm" value="(.*?)" />', html)
    sbdm = re.findall(r'<input type="hidden" name="sbdm" value="(.*?)" />', html)
    pAutoID = re.findall(r'<input type="hidden" name="pAutoID" value="(.*?)" />', html)
    page = re.findall(r'<input type="hidden" name="page" value="(.*?)" />', html)
    ko = re.findall(r'<input type="hidden" name="ko" id="ko" value="(.*?)">', html)

    second_body = {
        'inputcode': captcha,
        'sshcode': ssh_code,
        '_hphm': _hphm[0],
        'sbdm': sbdm[0],
        'pAutoID': pAutoID[0],
        'page': page[0],
        'ko': ko[0]
    }
    second_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Referer': 'http://www.hbgajg.com/service/show-12-42.html',
        'Origin': 'http://www.hbgajg.com',
        'Host': 'www.hbgajg.com'
    }
    result = session.post(check_url, data=second_body, headers=second_headers)
    result.encoding = result.apparent_encoding
    end_result = result.text

    totle = re.findall(r'<span>（总计：<b>(.*?)</b> 条违法记录,记 <b>(.*?)</b> 分,罚款 <b>(.*?)</b> 元）</span>', end_result)

    value = []
    result_map = {'违章记录总数': totle[0][0], '总扣分': totle[0][1], '总罚款': totle[0][2]}
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
