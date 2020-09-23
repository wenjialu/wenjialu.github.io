import time
# 1. 导入模块
from selenium import webdriver
# 2. 创建浏览器对象
# 参数驱动路径
browser = webdriver.Chrome(executable_path='/Users/lujiawen/Library/Python/3.7/chromedriver')
# 3. 输入网址
browser.get("http://books.czwblog.com/iframe1.html")
print("切换前:",browser.page_source)
print("*"*100)
# 切换 iframe
# 1> 获取iframe 元素对象
iframe_element = browser.find_element_by_id('iframe2')
# 2> 切换 iframe
browser.switch_to.frame(iframe_element)
print("切换后:",browser.page_source)
print("*"*100)
# 3> 切换回 主窗口
browser.switch_to.default_content()
print("切回后:",browser.page_source)
time.sleep(5)
# 最后 退出浏览器
browser.quit()