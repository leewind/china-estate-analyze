# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpidersKeList(scrapy.Item):
    # define the fields for your item here like:
    city = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    district = scrapy.Field()
    hotpot= scrapy.Field()
