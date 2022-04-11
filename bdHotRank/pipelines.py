# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#存储到json
import json
#codecs处理文件和编码
import codecs
#异步入库
from twisted.enterprise import adbapi
import datetime
from pymysql import cursors
#同步入库
import MySQLdb

class BdhotrankPipeline(object):
    def process_item(self, item, spider):
        return item

#同步入库
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(
            "127.0.0.1",
            'root',
            '12345678',
            'bd_spider',
            charset="utf8",
            use_unicode=True
        )
        self.cursor = self.conn.cursor()
        
    def process_item(self, item, spider):
        insertSQL = """
            insert into hotrank(tab,title,heat,imgurl,crawtime)
            values (%s, %s, %s, %s, %s)
        """
        poly = dict(item)
        for i in range(len(poly["title"])):
            polyInsert = {
                "tab":poly["tab"],
                'title':poly["title"][i], 
                'heat':poly["heat"][i], 
                'imgurl':poly["imgurl"][i], 
                'crawtime':poly["crawtime"]
                }       
            self.cursor.execute(insertSQL, (polyInsert["tab"],polyInsert["title"],polyInsert["heat"],
                                     polyInsert["imgurl"],polyInsert["crawtime"]))
            self.conn.commit()
        
        return item

class JsonPipeline(object):
    #持久化存储到本地json
    def __init__ (self):
        # 打开文件
        self.file = codecs.open("article.json", "a", encoding="utf-8")
    
    def process_item(self, item, spider):
        poly = dict(item)
        for i in range(len(poly["title"])):
            polyInsert = {
                "tab":poly["tab"],
                'title':poly["title"][i], 
                'heat':poly["heat"][i], 
                'imgurl':poly["imgurl"][i], 
                'crawtime':poly["crawtime"]
                }
            lines = json.dumps(polyInsert, ensure_ascii=False) + "\n"
            self.file.write(lines)
        return item
    
    def spider_closed(self, spider):
        self.file.close()
# 异步入库       
class MysqlTwistedPipeline(object):
    def __init__(self):
        params = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '12345678',
            'charset': 'utf8',
            'database': 'bd_spider',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool("pymysql", **params) # 连接配置
        self.sql = """
                    insert into hotrank(tab,title,heat,imgurl,crawtime)
                    values(%s,%s,%s,%s,%s)
                    """
    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_sql, item) # scrapy 带的异步连接池
        defer.addErrback(self.handle_err, item, spider) # 错误处理的回调

    def insert_sql(self,cursor,item):
        poly = dict(item)
        for i in range(len(poly["title"])):
            polyInsert = {
                "tab":poly["tab"],
                'title':poly["title"][i], 
                'heat':poly["heat"][i], 
                'imgurl':poly["imgurl"][i], 
                'crawtime':poly["crawtime"]
                }
            cursor.execute(self.sql,(polyInsert["tab"],polyInsert["title"],polyInsert["heat"],
                                     polyInsert["imgurl"],polyInsert["crawtime"]))

    def handle_err(self, error, item, spider):
        if error:
            print("INFO:%s %s"%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),error))       