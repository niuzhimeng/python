import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify  # 导入Flask类
from flask import request
import time
app = Flask(__name__)  # 创建Flask类的一个实例


@app.route("/phone", methods=['get'])
def index():
    phone = request.args.get('phone')
    url = 'http://www.ip138.com:8080/search.asp?mobile=' + phone + '&action=mobile'
    page = requests.get(url)
    time.sleep(0.3)
    page.encoding = 'gbk'
    info = BeautifulSoup(page.text, 'lxml')
    pageInfo = info.find_all('td', attrs={'align': 'center'})
    list = []
    for info in pageInfo[2::2]:
        if len(info.text) > 10:
            list.append(info.text.split(' ')[0])
        else:
            list.append(info.text)
    result = {'phoneNumber': list[0], 'city': list[1], 'cardType': list[2], 'areaCode': list[3], 'postCode': list[4]}

    return jsonify(result)


if __name__ == '__main__':  # Python入口程序
    app.run(host='192.168.3.213', port=8090, debug=False)  # 使其运行于本地服务器上
