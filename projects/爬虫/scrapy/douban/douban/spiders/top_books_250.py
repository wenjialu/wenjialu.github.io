import bs4
import scrapy
from ..items import DoubanItem, DangdangItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['book.douban.com']
    start_urls = []
    for x in range(1,4):
        # url = 'https://book.douban.com/top250?start=' + str(x * 25)
        url = 'http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-year-2018-0-1-%s' %x
        start_urls.append(url)

    def parse(self, response):
        bs = bs4.BeautifulSoup(response.text, 'html.parser')
        # 用BeautifulSoup解析response。

        # datas = bs.find_all('tr', class_="item")
        # 用find_all提取<tr class="item">元素，这个元素里含有书籍信息。
        # for data in datas:
        #     # item = DoubanItem()
        #     # 实例化DoubanItem这个类。
        #     # item['title'] = data.find_all('a')[1]['title']
        #     # # 提取出书名，并把这个数据放回DoubanItem类的title属性里。
        #     # item['publish'] = data.find('p', class_='pl').text
        #     # # 提取出出版信息，并把这个数据放回DoubanItem类的publish里。
        #     # item['score'] = data.find('span', class_='rating_nums').text
        #     # # 提取出评分，并把这个数据放回DoubanItem类的score属性里。
        #     # print(item['title'])
        #     # yield item
        #     # yield item是把获得的item传递给引擎。
        # print(response.text)

        item = DangdangItem()
        books = bs.find_all('ul',class_='bang_list clearfix bang_list_mode')
        for book in books: #h前3个页面的这个标签里面去找。
            li =book.find_all('li')  #一下找到20本书
            for i in li: #只打印3本书说明只走了外层3次循环，内循环失效了。
                item['name'] = i.find_all('a')[1]['title']
                # item['name'] = i.find('div',class_='name').text #和上面效果一样诶，不知道哪个快。
                item['author'] = i.find_all('a')[3]['title']
                item['price'] = i.find('span',class_='price_n').text #可以直接找到循环里同级再下一级的内容诶！！
                yield item
                print(item['name'])
                print('-----------')
            print('————————————————————————————————————————————')
        print('====================================') #这里的效果/循环位置是不是和上面"——————"一样的啊晕