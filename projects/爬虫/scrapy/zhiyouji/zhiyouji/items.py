# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class JobuiItem(scrapy.Item):
    # 定义了一个继承自scrapy.Item的JobuiItem类
    company = scrapy.Field()
    # 定义公司名称的数据属性
    position = scrapy.Field()
    # 定义职位名称的数据属性
    address = scrapy.Field()
    # 定义工作地点的数据属性
    detail = scrapy.Field()
    # 定义招聘要求的数据属性