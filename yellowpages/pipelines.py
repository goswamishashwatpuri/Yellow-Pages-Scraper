# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import sqlite3
import pymongo
import dnspython





# class SqliteYellowPagesPipeline(object):

#     def open_spider(self, spider):
#         self.connection = sqlite3.connect("leads.db")

#         self.cur = self.connection.cursor()
#         self.cur.execute ("""
#             CREATE TABLE leads(
#                 title TEXT,
#                 contact TEXT,
#                 tags TEXT,
#                 website TEXT,
#                 address TEXT
#                 )
#             """)
#         self.connection.commit()

#     def process_item(self, item, spider):

#         self.cur.execute("""
#             INSERT INTO leads (title,contact,tags,website,address) VALUES (?,?,?,?,?) """
#             , (
#                 item.get('Title'), 
#                 item.get('Contact'), 
#                 item.get('Tags'), 
#                 item.get('Website'), 
#                 item.get('Address')
#               )
#             )
#         self.connection.commit()
#         return item

#     def close_spider(self, spider):
#         self.connection.close()    


class MongoYellowPagesPipeline(object):



    def __init__(self, container = 'container123'):

        self.container_name = input("enter container name")
        if self.container_name == '':
            self.container_name = container

    def open_spider(self, spider):

        self.client = pymongo.MongoClient("client connection link here")
        self.db = self.client['yellowpagesdb'] 

    def process_item(self, item, spider):

        self.db[self.container_name].insert(item)
        return item

    def close_spider(self, spider):

        print("YOUR DATABASE NAME IS : ", self.container_name)
        self.client.close()      