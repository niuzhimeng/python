import re
import time

import requests
from PIL import Image

session = requests.session()


def check():
    check_url = 'http://www.hbgajg.com/service/show-12-42.html'
    check_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Host': 'www.hbgajg.com',
        'Origin': 'http://www.hbgajg.com',
        'Referer': 'http://www.hbgajg.com/'
    }
    check_body = {
        'CC_JDCWZ_OneArea': '11',
        'CC_JDCWZ_OneZimu': '18',
        'CC_JDCWZ_Two': 'X0537',
        'CC_JDCWZ_Three': '02',
        'CC_JDCWZ_Four': '1885',
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
    print(result.text)


if __name__ == '__main__':
    check()
