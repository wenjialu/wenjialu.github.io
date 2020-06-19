
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome(executable_path='/Users/lujiawen/Library/Python/3.7/chromedriver')
driver.get('http://114.67.96.222:9000')

time.sleep(2)
title=driver.find_element_by_tag_name('h1')
# try:
#     print(title.text)
#     # title.send_keys(Keys.ENTER)
#     # title.send_keys('你已被攻击！！！')
#     # time.sleep(1)
#     # title.clear()
# except:
driver.close()




