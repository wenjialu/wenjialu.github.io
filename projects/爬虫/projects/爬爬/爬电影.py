

import requests
from bs4 import BeautifulSoup
# 思路一：找最小父集
# for page in range(1,10):
#     res = requests.get('https://movie.douban.com/top250?start=%s&filter=' %((page-1)*25))
#     html_content = res.text
#     bs_content = BeautifulSoup(html_content,'html.parser' )
#     tag_comment = bs_content.find_all('div',class_='item')
#     # print(tag_comment)
#     list = []
#     #法一：切片法
#     for item in tag_comment:
#         # print('遍历 的元素是',item)
#         seq = item.find('em',class_='').text
#         name = item.find('span',class_='title').text
#         rate = item.find('span',class_='rating_num').text
#         com = item.find('span',class_='inq').text
#         list.append(['序号：%s,名字：%s,评分：%s, 评价:%s' %(seq,name,rate,com)])
#     for i in list:
#         print(i)


#思路二：分别提取所有的序号/所有的电影名/所有的评分/所有的推荐语/所有的链接，然后再按顺序一一对应起来。
for page in range(1,10):
    res = requests.get('https://movie.douban.com/top250?start=%s&filter=' %((page-1)*25))
    html_content = res.text
    bs_content = BeautifulSoup(html_content,'html.parser' )
    seq = bs_content.find_all('em', class_='')
    name = bs_content.find_all('span', class_='title')
    rate = bs_content.find_all('span', class_='rating_num')
    com = bs_content.find_all('span', class_='inq')

    list = []
    #法一：切片法
    for x in range(len(seq)):
        list.append(['序号：%s,名字：%s,评分：%s, 评价:%s' %(seq[x].text,name[x].text,rate[x].text,com[x].text)])
    for i in list:
        print(i)






