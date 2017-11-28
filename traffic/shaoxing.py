import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)
session = requests.session()


@app.route("/check_traffic_shaoxing", methods=['GET', 'POST'])
def check():
    fdj = request.values.get('fdj')
    car_number = request.values.get('carNumber')
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Content-Length': '45',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Host': 'wscgs.sxga.gov.cn',
        'Origin': 'http://wscgs.sxga.gov.cn',
        'Referer': 'http://wscgs.sxga.gov.cn/index',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    data = {
        'hpzl': '02',
        'fzjgjc': car_number[0].encode('gbk'),
        'hphm': car_number[1:],
        'fdjh': fdj
    }
    url = 'http://wscgs.sxga.gov.cn/viocheck/viocheck.do?act=Vehviohlist'
    html = session.post(url, headers=header, data=data)
    html.encoding = html.apparent_encoding
    f_soup = BeautifulSoup(html.text, 'lxml')
    tables = f_soup.find_all('table', class_='diaryTable')
    tr = tables[1].find_all('tr')
    tr0 = tables[0].find_all('tr')

    value0 = []
    for r0 in tr0:
        for d0 in r0.find_all('td'):
            value0.append(d0.get_text().strip())
    print(value0)
    result_map = {value0[0]: value0[1], value0[2]: value0[3], value0[4]: value0[5], value0[6]: value0[7],
                  value0[8]: value0[9]}
    value = []
    for r in tr[1:]:
        for d in r.find_all('td'):
            value.append(d.get_text().strip().replace('□', ''))

    k = 0
    result_value = []
    for i in range(0, int(len(value) / 6)):
        dic = {
            '违法日期': value[k],
            '违法地点': value[k + 1],
            '违法行为': value[k + 2],
            '处理状态': value[k + 3],
            '采集机关': value[k + 4]
        }
        k += 6
        result_value.append(dic)

    result_map['违章详情'] = result_value
    return jsonify(result_map)


if __name__ == '__main__':
    app.run(host='192.168.3.213', port=8090, debug=False)
