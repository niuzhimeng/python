"""
实现页面下拉
"""

from selenium import webdriver
from time import sleep

driver = webdriver.PhantomJS()
driver.get('http://www.jianshu.com')
driver.maximize_window()
sleep(2)
# 这个是你下拉多少像素
driver.execute_script("window.scrollBy(0,4800)")
# 下拉后休眠一秒
sleep(1)
# 得到网页中的数据
demo = driver.page_source
print(demo)
