# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import SpidersKeList
import urllib

class SpiderPipeline(object):

    username_str = 'breadt'
    password_str = 'Breadt@2019'

    def connect(self):

        username = urllib.parse.quote_plus(self.username_str)
        password = urllib.parse.quote_plus(self.password_str)

        self.client = pymongo.MongoClient('mongodb://%s:%s@10.12.86.109:27017/' % (username, password))
        self.db = self.client["ke"]

    def open_spider(self, spider):
        print('SpidersPipeline.open_spider')
        self.connect()

    def process_item(self, item, spider):

        if isinstance(item, SpidersKeList):
            feedback = self.db["kelist"].insert_one({'content': item['content'], 'date': item['date']})

        return item

    def close_spider(self, spider):
        self.client.close()
