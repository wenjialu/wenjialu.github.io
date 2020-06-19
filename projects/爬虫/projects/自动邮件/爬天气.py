import requests
from bs4 import BeautifulSoup

headers={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
#封装headers
url='http://www.weather.com.cn/weather/101280601.shtml'
#把URL链接赋值到变量url上。
res=requests.get(url,headers=headers)
#发送requests请求，并把响应的内容赋值到变量res中。
res.encoding = 'utf-8'
print(res.status_code)
#检查响应状态是否正常
print(res.text)
#打印出res对象的网页源代码