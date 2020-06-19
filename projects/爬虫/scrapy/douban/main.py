from scrapy import cmdline
#导入cmdline模块,可以实现控制终端命令行。
cmdline.execute(['scrapy','crawl','douban'])
#用execute（）方法，输入运行scrapy的命令。