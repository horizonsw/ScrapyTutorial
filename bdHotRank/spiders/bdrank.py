# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from ..items import BaiduHotNewsItem

class BdrankSpider(scrapy.Spider):
    name = 'bdrank'
    allowed_domains = ['top.baidu.com']
    start_urls = ['https://top.baidu.com/board?tab=realtime']
    headers = {
        "HOST": "top.baidu.com",
        "USER_AGENT":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }

    def parse(self, response):
        #
        item_loader = ItemLoader(item=BaiduHotNewsItem(), response=response)
        item_loader.add_value("tab",response.url.split("=")[1])
        item_loader.add_xpath("title","//div[contains(@class,'category-wrap_iQLoo')]//div[@class='c-single-text-ellipsis']/text()")
        item_loader.add_xpath("heat","//div[contains(@class,'category-wrap_iQLoo')]//div[@class='hot-index_1Bl1a']/text()")
        item_loader.add_xpath("imgurl","//div[contains(@class,'category-wrap_iQLoo')]/a/img/@src")
        item_loader.add_value("crawtime",'')
        
        HotRankItem = item_loader.load_item()    
        yield HotRankItem
        
    
    def start_requests(self):
        #入口
        for i in ["realtime","novel","movie","teleplay","car","game"]:
            contUrl = "https://top.baidu.com/board?tab={}".format(i)
            yield scrapy.Request(contUrl,headers=self.headers,dont_filter=True,callback=self.parse)    

        