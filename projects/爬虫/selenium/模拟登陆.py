
import time

from selenium import webdriver

driver = webdriver.Chrome(executable_path='/Users/lujiawen/Library/Python/3.7/chromedriver')
driver.get('https://wordpress-edu-3autumn.localprod.forc.work/wp-login.php')
time.sleep(1)



username = driver.find_element_by_id('user_login')
username.send_keys('spiderman')
pw = driver.find_element_by_id('user_pass')
pw.send_keys('crawler334566')
time.sleep(1)
buttom = driver.find_element_by_id('wp-submit')
buttom.click()



article = driver.find_element_by_id('post-20').find_element_by_class_name('entry-title').find_element_by_tag_name('a')
article.click()
time.sleep(2)

comment = driver.find_element_by_id('comment')
comment.send_keys('我是秀儿，我会用selenium')
submit = driver.find_element_by_id('submit')
submit.click()

time.sleep(4)
driver.close()