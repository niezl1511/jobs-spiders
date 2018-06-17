# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import csv
# 引入settings的所有配置
from scrapy.utils.project import get_project_settings
import pymysql

class CrawlspiderdemoPipeline(object):

    def open_spider(self,spider):
        self.jsonfile = open("dushu.json",'w',encoding='utf-8')
        self.csvfile = open("dushu.csv",'w',encoding='utf-8')
        self.items = []
        self.csv_items = []


    def process_item(self, item, spider):
        dic = dict(item)
        self.items.append(dic)

        # 整合csv数据
        csv_item = []
        csv_item.append(item["title"])
        csv_item.append(item["author"])
        csv_item.append(item["info"])
        csv_item.append(item["img_url"])

        self.csv_items.append(csv_item)

        return item

    def close_spider(self,spider):
        self.jsonfile.write(json.dumps(self.items))
        self.jsonfile.close()
        # 写入csv
        writer = csv.writer(self.csvfile)
        writer.writerow(["title","author","info","img_url"])
        writer.writerows(self.csv_items)



# 练习：把这些数据写入csv

# 添加一个自定义的管道类
class Mysqlpipe(object):

    def __init__(self):
        # 引入settings文件
        settings = get_project_settings()
        self.host = settings["DB_HOST"]
        self.port = settings["DB_PORT"]
        self.user = settings["DB_USER"]
        self.pwd = settings["DB_PASSWORD"]
        self.name = settings["DB_NAME"]
        self.charset = settings["DB_CHARSET"]
        self.connectDB()

    # 创建一个函数，用于链接数据库
    def connectDB(self):
        self.con = pymysql.connect(host=self.host,
                                   port=self.port,
                                   user=self.user,
                                   password=self.pwd,
                                   db=self.name,
                                   charset=self.charset
                                   )
        # 创建游标
        self.cursor = self.con.cursor()

    def process_item(self,item,spider):
        # 在这里我们将item写入数据库
        sql = "INSERT INTO  dushutable VALUES (NULL,'%s','%s','%s','%s')" % (item['title'],item['author'],item["info"],item['img_url'])
        # print("======================================")
        # print(sql)
        # 执行sql语句
        self.cursor.execute(sql)

        self.con.commit()
        return item

    def close_spider(self,spider):
        self.con.close()
        self.cursor.close()
