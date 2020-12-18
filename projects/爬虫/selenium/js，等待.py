

# # 教学系统的浏览器设置方法
# from selenium.webdriver.chrome.webdriver import RemoteWebDriver # 从selenium库中调用RemoteWebDriver模块
# from selenium.webdriver.chrome.options import Options # 从options模块中调用Options类
# import time
#
# chrome_options = Options() # 实例化Option对象
# chrome_options.add_argument('--headless') # 对浏览器的设置
# driver = RemoteWebDriver("http://chromedriver.python-class-fos.svc:4444/wd/hub", chrome_options.to_capabilities()) # 声明浏览器对象
import time

from selenium import webdriver




driver = webdriver.Chrome(executable_path='/Users/lujiawen/Library/Python/3.7/chromedriver')

driver.get('https://localprod.pandateacher.com/python-manuscript/hello-spiderman/') # 访问页面
# time.sleep(2) # 等待2秒
# label = driver.find_element_by_tag_name('label') # 解析网页并提取第一个<lable>标签
# print(label) # 打印label
# print(label.text) # 打印label的文本
# print(type(label)) # 打印label的数据类型

#find_element只会返回第一个
label = driver.find_element_by_class_name('teacher') # 根据类名找到元素

#隐式等待
driver.implicity_wait(5)
js = driver.execute_script('scrollTO(0,10)')


driver.close() # 关闭浏览器
