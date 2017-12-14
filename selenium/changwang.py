from time import sleep
import time
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
sleep(1)

# 登录成功后 获取输入框对象
carnumber = driver.find_element_by_name('carnumber')
carframe = driver.find_element_by_name('carframe')
verify = driver.find_element_by_name('verify')
query_car_sub = driver.find_element_by_class_name('query_car_sub')

# 获取验证码
t = str(int(time.time() * 1000))
yzm_url = 'http://www.cwddd.com/Common/verify?ran=' + t
driver.get(yzm_url)
driver.maximize_window()
driver.save_screenshot('yzm.png')
y = input('yzm: ')

# input框赋值
carnumber.send_keys('川A59ZT5')
carframe.send_keys('170943')
verify.send_keys(y)
# 点击查询按钮
query_car_sub.click()
sleep(3)
print(driver.page_source)
