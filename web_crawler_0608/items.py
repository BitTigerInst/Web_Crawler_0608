# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebCrawler0608Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class TruliaWebCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    href = scrapy.Field()
    mortgage_id = scrapy.Field()
    mortgage_value = scrapy.Field()
    neighborhood = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
    bedroom = scrapy.Field()
    bathroom = scrapy.Field()
#    sqft = scrapy.Field()
