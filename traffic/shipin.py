import uuid

import pymysql
import requests
from flask import json

session = requests.session()
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='nzm19940827',
                             db='amdb',
                             charset='utf8')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
try:
    for index in range(1, 271):

        data = {
            'page': index
        }
        html = session.post('http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsList', headers=headers,
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
            data1 = {
                'id': list[i]['ID']
            }
            response = session.post('http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsById', data=data1,
                                    headers=headers)

            res1 = json.loads(response.text)
            # 点击后获得的内容
            certStr = res1['certStr']  # 许可项目
            epsAddress = res1['epsAddress']  # 企业住所
            epsProductAddress = res1['epsProductAddress']  # 生产地址
            businessLicenseNumber = res1['businessLicenseNumber']  # 社会信用代码
            legalPerson = res1['legalPerson']  # 法定代表人
            businessPerson = res1['businessPerson']  # 企业负责人
            qualityPerson = res1['qualityPerson']  # 质量负责人
            rcManagerDepartName = res1['rcManagerDepartName']  # 日常监督管理机构
            rcManagerUser = res1['rcManagerUser']  # 日常监督管理人员
            xkName = res1['xkName']  # 签发人
            with connection.cursor() as cursor:
                sql = 'insert into food(id, company_name, licence, send_paper, validity_date, send_paper_time,' \
                      'certStr, epsAddress, epsProductAddress, businessLicenseNumber, legalPerson, businessPerson, qualityPerson, rcManagerDepartName, rcManagerUser,xkName)' \
                      ' values(%s, %s, %s, %s,%s, %s,%s, %s, %s, %s,%s, %s,%s, %s, %s, %s)'
                cursor.execute(sql, (int(uuid.uuid1()), name, licence, send_paper, validity_date, send_paper_time,
                                     certStr, epsAddress, epsProductAddress, businessLicenseNumber, legalPerson,
                                     businessPerson, qualityPerson, rcManagerDepartName, rcManagerUser,xkName))
        # 事务提交
        connection.commit()
finally:
    # 关闭数据库连接
    connection.close()
