import requests

data = {
    'id': '86b60fb7df4e4be9bac1350557227352'
}
response = requests.post('http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsById', data=data)
html = response.text
print(html)
