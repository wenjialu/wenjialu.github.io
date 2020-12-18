from gevent import monkey
monkey.patch_all()  #变成异步、
import gevent,time,requests
from gevent.queue import Queue
from bs4 import BeautifulSoup
start = time.time()


work = Queue()
url_list = ['http://www.mtime.com/top/tv/top100/']
for i in range(1,10):
    url = 'http://www.mtime.com/top/tv/top100/index-%s.html' %(i+1)
    url_list.append(url)
for url in url_list:
    work.put_nowait(url)


def crawler():
    while not work.empty():
        url = work.get_nowait()
        r = requests.get(url)
        # print(url,work.qsize(),r.status_code)
        #爬页面内容
        bs_content = BeautifulSoup(r.text, 'html.parser')
        list_all = bs_content.find_all('ul',id='asyncRatingRegion')
        # content_all = bs_content.find_all('div',class_='mov_con')
        name = bs_content.find('a', class_='c_blue')
        # actor = bs_content.find('h2', class_='c_blue')
        comment = bs_content.find('p', class_='mt3')
        list=[]
        for x in range(len(list_all)):
            print('名字:%s，/n 评价:%s' % (name.text, comment.text))



tasks_list = []
for x in range(2):
    #导入了gevent库来帮我们实现多协程
    #crawler函数里面才是真的在爬虫，这个gevent只是开个携程把任务放进去。
    task = gevent.spawn(crawler)
    '''gevent只能处理gevent的任务对象，不能直接调用普通函数，
         所以需要借助gevent.spawn()来创建任务对象。把函数和参数传到gevent对象里。'''
    tasks_list.append(task)

gevent.joinall(tasks_list)
end = time.time()
print(end-start)