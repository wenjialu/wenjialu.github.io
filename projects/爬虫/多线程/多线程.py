#线程池
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

def pachong(name):
    url='http://114.67.96.222:9000'
    res = requests.get(url)
    html_content = res.text
    bs_content = BeautifulSoup(html_content, 'html.parser')
    indexs = bs_content.find_all('ul')
    for index in indexs:
        print("*"*10)
        print(name)
        print(indexs)
        print("*" * 10)


if __name__ == '__main__':
  pool = ThreadPoolExecutor(2000)
  for i in range(1,1000):
    pool.submit(pachong('lulu'+str(i)))

