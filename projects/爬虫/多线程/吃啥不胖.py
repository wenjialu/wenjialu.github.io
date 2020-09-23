

# 用for循环构造出前3个常见食物类别的前3页食物记录的网址和
# 第11个常见食物类别的前3页食物记录的网址
import csv

from bs4 import BeautifulSoup
from gevent import monkey
monkey.patch_all()  #变成异步、
import gevent,time,requests
from gevent.queue import Queue
start = time.time()

work = Queue()

url_1 = 'http://www.boohee.com/food/group/{type}?page={page}'
for i in range(1,4):
    for j in range(1,4):
        real_url = url_1.format(type=i, page=j)
        work.put_nowait(real_url)

url_11='http://www.boohee.com/food/view_menu?page={page}'
for i in range(1,4):
    real_url = url_11.format(page=i)
    work.put_nowait(real_url)

#测试-打印队列
# print(work)
#
def crawler():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }
    while not work.empty():
        url = work.get_nowait()
        r = requests.get(url, headers=headers)
        print(url,work.qsize(),r.status_code)

        bs_content = BeautifulSoup(r.text, 'html.parser')
        list_all = bs_content.find_all('li', class_='item clearfix')

        for x in list_all:
            name = x.find_all('a')[1]['title']  #这句话重点啊 学习领悟参透
            cal = x.find('p').text
            food_url = 'http://www.boohee.com' + x.find_all('a')[1]['href']
            writer.writerow([name, cal, food_url])
            print('食物:%s， 热量:%s， 链接%s' % (name, cal,food_url))

csv_file= open('吃啥不胖.csv', 'w', newline='',encoding='utf-8')
#调用open()函数打开csv文件，传入参数：文件名“boohee.csv”、写入模式“w”、newline=''。
writer = csv.writer(csv_file)
# 用csv.writer()函数创建一个writer对象。
writer.writerow(['食物', '热量', '链接'])


tasks_list = []
for x in range(5):
    task = gevent.spawn(crawler)
    '''gevent只能处理gevent的任务对象，不能直接调用普通函数，
         所以需要借助gevent.spawn()来创建任务对象。把函数和参数传到gevent对象里。'''
    tasks_list.append(task)

gevent.joinall(tasks_list)




end = time.time()
print(end-start)

