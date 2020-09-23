import requests
from bs4 import BeautifulSoup
import re
res = requests.get('http://www.xiachufang.com/explore/') #得到响应<Response[200]>，详见调试
html_content = res.text
bs_content = BeautifulSoup(html_content,'html.parser' ) #得到bs对象：bs把text字符串解析了。
tag_comment = bs_content.find_all('div',class_='info pure-u') #bs对象的方法有find_all,能找符合条件的标签
print(type(tag_comment)) #对象
list = []
# 法一：切片法
for item in tag_comment: #一个<div>一道菜</div>块   #for x in range（）。#x用来计数
	# print('遍历 的元素是',item)
	name = item.find('p',class_='name').text #item还是bs对象，有find方法。
	receipe = item.find('p',class_='ing ellipsis').text
	list.append(['菜名：%s,配方：%s' %(name,receipe)])
print(list)
# xpath


#法二：正则
for item in tag_comment:     #for food in XXX。#food是遍历可迭代对象XXX（我猜可能是tag），可以被调用（如：food.find）。
	# print('遍历 的元素是',item)
	name_rol = item.find('p',class_='name').text
	receipe_rol = item.find('p',class_='ing ellipsis').text
	name = re.sub('\n\n*','',name_rol)
	receipe = re.sub('\n\n*','',receipe_rol)
	list.append(['菜名：%s     配方：%s' %(name,receipe)])
for i in list:
	print(i)

print(list)


