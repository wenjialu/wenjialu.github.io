from gevent import monkey
monkey.patch_all()  #变成异步、
import gevent,time,requests
from gevent.queue import Queue
start = time.time()

url_list = ['https://www.baidu.com/',
'https://www.sina.com.cn/',
'http://www.sohu.com/',
'https://www.qq.com/',
'https://www.163.com/',
'http://www.iqiyi.com/',
'https://www.tmall.com/',
'http://www.ifeng.com/']

work = Queue()

for url in url_list:
    work.put_nowait(url)


def crawler():
    while not work.empty():
        url = work.get_nowait()
        r = requests.get(url)
        print(url,work.qsize(),r.status_code)


tasks_list = []
for x in range(2):
    #导入了gevent库来帮我们实现多协程
    #gevent只能处理gevent的任务对象，不能直接调用普通函数，
    # 所以需要借助gevent.spawn()来创建任务对象。把函数和参数传到gevent对象里。
    task = gevent.spawn(crawler)
    tasks_list.append(task)

gevent.joinall(tasks_list)
end = time.time()
print(end-start)


