import requests
from bs4 import BeautifulSoup


def get():
    page = requests.session().get('http://www.budejie.com/text/15', headers={'User-Agent':
                                                                                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'})

    pageInfo = BeautifulSoup(page.text, 'html.parser')

    div = pageInfo.find_all('div', 'j-r-list-c-desc')

    for i in range(0, div.__len__()):
        s = str(div[i].a.get_text())
        if s.__len__() > 70:
            print('(' + str(i + 1) + ') ' + huanhang(s))

        else:
            print('(' + str(i + 1) + ') ' + s + '\r\n')


def huanhang(temp):
    text = ''
    while temp:
        text = text + temp[:78] + "\r\n"
        temp = temp[78:]
    return text


if __name__ == '__main__':
    get()
