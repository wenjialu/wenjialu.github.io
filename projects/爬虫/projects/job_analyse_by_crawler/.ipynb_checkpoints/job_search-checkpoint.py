# -*- coding: utf-8 -*-
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
cookies = {'cookie':'__zp__pub__=; __c=1591717214; __g=-; __l=l=%2Fwww.zhipin.com%2F&r=https%3A%2F%2Fwww.google.com%2F&friend_source=0&friend_source=0; lastCity=100010000; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1591717215,1592275348; __a=64681111.1591717214..1591717214.51.1.51.51; __zp_stoken__=3638aKTs6azs8RQV1QVtLEA5rPGs7TC4YB3kqDANpchkQJ2s1QVphESVQLhBiTH8hfiA6MVldZ2VvMHFVE0ceQXFJNnMjOiIzWU9VIzI8N2NdRwlRLSxxS2YUKgoTNwlqPBl%2FTiRbDRgtfnQ%3D; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1592275469'}

res = requests.get('https://www.zhipin.com/c100010000/?query=%E6%95%B0%E6%8D%AE%E5%AE%9E%E4%B9%A0&page=1',cookies=cookies)
html_content = res.text
bs_content = BeautifulSoup(html_content,'html.parser' )
sal = bs_content.find_all(class_='red')
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
