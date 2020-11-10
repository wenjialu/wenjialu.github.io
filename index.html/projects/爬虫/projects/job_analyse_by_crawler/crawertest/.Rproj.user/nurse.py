import requests
# from lxml import etree
import time
import random
import pandas as pd
import re
from bs4 import BeautifulSoup

#         招聘网站：(boss,拉勾，猎聘，前程无忧)
#             公司名
#             所在地
#             规模
#             岗位
#             薪资
#             链接
#             要求：
#                 学历
#                 经验
#                 技能

requests.packages.urllib3.disable_warnings()

# headers ={
    # user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36
# }

res = requests.get('http://zh.zhhlzzs.com/CN/0254-1769/current.shtml')
html_content = res.text
bs_content = BeautifulSoup(html_content,'html.parser' )
sal = bs_content.find_all(class_='MsoNormal')
# print(html_content)
print(sal)
# for item in tag_comment:
#    # print('遍历 的元素是',item)
# 	cm = item.find('p')
# 	print(cm.text)







# def get_zwurls(url):
#     try:
#         zwurls=[]
#         res = requests.get(url,headers=headers)
#         res.encoding = 'GBK'
#         html = etree.HTML(res.text)
#         data = html.xpath('//div[@class="dw_table"]/div[@class="el"]')
#         for i in data:
#             zwurls = i.xpath(string( )  )