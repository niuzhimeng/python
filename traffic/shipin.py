import requests
from flask import json
import uuid

import pymysql

connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='nzm19940827',
                             db='amdb',
                             charset='utf8')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}
try:
    for index in range(1, 271):

        data = {
            'page': index
        }
        html = requests.post('http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsList', headers=headers,
                             data=data)
        res = json.loads(html.text)
        list = res['list']
        for i in range(int(len(list))):
            name = list[i]['EPS_NAME']  # 企业名称
            licence = list[i]['PRODUCT_SN']  # 许可证编号
            send_paper = list[i]['QF_MANAGER_NAME']  # 发证机关
            validity_date = list[i]['XK_DATE']  # 有效期
            send_paper_time = list[i]['XC_DATE']  # 发证期
            # 获得数据库游标
            with connection.cursor() as cursor:
                sql = 'insert into food(id, company_name, licence, send_paper, validity_date, send_paper_time)' \
                      ' values(%s, %s, %s, %s,%s, %s)'
                cursor.execute(sql, (int(uuid.uuid1()), name, licence, send_paper, validity_date, send_paper_time))
        # 事务提交
        connection.commit()
finally:
    # 关闭数据库连接
    connection.close()
