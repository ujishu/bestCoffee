# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BestcoffeeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    time = scrapy.Field()
    title = scrapy.Field()
    product_url = scrapy.Field()
    image_url = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    site = scrapy.Field()
    location = scrapy.Field()
    product_rating = scrapy.Field()
