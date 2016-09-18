# -*- coding: utf-8 -*-

import pymongo
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class WebCrawler0608Pipeline(object):
#     def process_item(self, item, spider):
#         return item


class TruliaMongodbPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        collection_name = item.__class__.__name__  # use itemName as the collectionName
        #self.db[collection_name].remove({})  # clean the collection when new crawling starts
        self.db[collection_name].insert(dict(item))
        return item
