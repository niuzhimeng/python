from time import sleep
from PIL import Image
from selenium import webdriver

driver = webdriver.PhantomJS()
driver.get('http://user.cwddd.com/Public/login')
userName = driver.find_element_by_name('username')
userName.send_keys('295290968@qq.com')

passWord = driver.find_element_by_name('password')
passWord.send_keys('nzm19940827')

sleep(1)
login = driver.find_element_by_class_name('lgsubmit')
login.click()
sleep(3)
driver.get('http://www.cwddd.com/Service/wfindex.html')

# 登录成功后 获取输入框对象
carnumber = driver.find_element_by_name('carnumber')
carframe = driver.find_element_by_name('carframe')
verify = driver.find_element_by_name('verify')
query_car_sub = driver.find_element_by_class_name('query_car_sub')

verify.click()
sleep(1)
driver.save_screenshot('yzm.png')

# 验证码截取
# element = driver.find_element_by_id('verifyinfo')
# left = element.location['x']
# top = element.location['y']
# right = element.location['x'] + element.size['width'] + 30
# bottom = element.location['y'] + element.size['height']

# im = Image.open('yzm.png')
# im = im.crop((left, top, right, bottom))
# im.save('yzm2.png')

y = input('yzm: ')
# input框赋值
carnumber.send_keys('川A59ZT5')
carframe.send_keys('170943')
verify.send_keys(y)
# 点击查询按钮
query_car_sub.click()
sleep(3)
print(driver.page_source)
