import random
from urllib.request import Request
from urllib.request import urlopen


def getContent(headers):
    """ 
    此函数用于抓取返回403禁止访问的网页 
    """
    random_header = random.choice(headers)

    """ 
    对于Request中的第二个参数headers，它是字典型参数，所以在传入时 
    也可以直接将个字典传入，字典中就是下面元组的键值对应 
    """
    req = Request('http://tools.2345.com/carlist.htm')
    req.add_header("User-Agent", random_header)
    content = urlopen(req).read().decode("gbk")
    return content

# 这里面的my_headers中的内容由于是个人主机的信息，所以我就用句号省略了一些，在使用时可以将自己主机的
my_headers = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"]
print(getContent(my_headers))
