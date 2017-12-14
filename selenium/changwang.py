from time import sleep

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
print(driver.page_source)
