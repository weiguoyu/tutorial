# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)


class DianpingItem(scrapy.Item):
    shop_name = scrapy.Field()
    shop_address = scrapy.Field()
    shop_region = scrapy.Field()
    shop_city = scrapy.Field()
    shop_latitude = scrapy.Field()
    shop_longitude = scrapy.Field()



