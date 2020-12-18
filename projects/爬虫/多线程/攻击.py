
from gevent import monkey
monkey.patch_all()  #变成异步模式
import gevent,time,requests

start = time.time()

url_list = ['https://www.baidu.com/',
'https://www.sina.com.cn/',
'http://www.sohu.com/',
'https://www.qq.com/',
'https://www.163.com/',
'http://www.iqiyi.com/',
'https://www.tmall.com/',
'http://www.ifeng.com/']

def crawler(url):
    r = requests.get(url)
    print(url,time.time()-start,r.status_code)


tasks_list = [ ]
#创建空的任务列表。
for i in range(1000):
    task = gevent.spawn(crawler,url_list[i*200:(i+1)*200])
    #用gevent.spawn()函数创建5个任务。
    tasks_list.append(task)
    #往任务列表添加任务。


gevent.joinall(tasks_list)
end = time.time()
print(end-start)


