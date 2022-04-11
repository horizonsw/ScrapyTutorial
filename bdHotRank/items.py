# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
from scrapy.loader.processors import MapCompose


class BdhotrankItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BaiduHotNewsItem(scrapy.Item):
    #bd前30热搜item
    # 榜单类型
    tab = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 热度
    heat = scrapy.Field()
    # 图片链接
    imgurl = scrapy.Field()
    # 爬取时间
    crawtime = scrapy.Field(
        input_processor = MapCompose(lambda x:datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

