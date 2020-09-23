
import time

from selenium import webdriver


driver = webdriver.Chrome(executable_path='/Users/lujiawen/Library/Python/3.7/chromedriver')
#无头 部署时候
driver = webdriver.PhantomJs()

driver.get('https://localprod.pandateacher.com/python-manuscript/hello-spiderman/')
time.sleep(2)

teacher = driver.find_element_by_id('teacher')
teacher.send_keys('必须是xx呀')
assistant = driver.find_element_by_name('assistant')
assistant.send_keys('都喜欢')
time.sleep(1)
button = driver.find_element_by_class_name('sub')
time.sleep(1)
button.click()
time.sleep(1)
driver.close()

# teacher = driver.find_element_by_id('teacher')
# print(type(teacher))
# teacher.send_keys('略乐乐')
# assistant = driver.find_element_by_name('assistant') # 找到【请输入你喜欢的助教】下面的输入框位置
# assistant.send_keys('都喜欢')
# submit=driver.find_element_by_class_name('sub')
# submit.click()
# driver.close()


