import time

from selenium import  webdriver #从selenium库中调用webdriver模块
from selenium.webdriver.chrome.options import Options # 从options模块中调用Options类

# driver = webdriver.Chrome(executable_path='/Users/lujiawen/Library/Python/3.7/chromedriver')

chrome_options = Options() # 实例化Option对象
chrome_options.add_argument('--headless') # 把Chrome浏览器设置为静默模式
driver = webdriver.Chrome(executable_path='/Users/lujiawen/Library/Python/3.7/chromedriver',options = chrome_options) # 设置引擎为Chrome，在后台默默运行



driver.get('https://y.qq.com/n/yqq/song/000xdZuV2LcQ19.html')
time.sleep(2)


button = driver.find_element_by_class_name('js_get_more_hot')
# print(more)
button.click()
time.sleep(4)

comments = driver.find_element_by_class_name('js_hot_list').find_elements_by_class_name('js_cmt_li')




for comment in comments:
    c = comment.find_element_by_tag_name('p')
    print('评论：%s\n------\n'%c.text)
driver.close()





