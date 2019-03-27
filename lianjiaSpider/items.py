# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



class lianjiaSpiderItem(scrapy.Item):
    house_title = scrapy.Field()
    house_href = scrapy.Field()
    house_add = scrapy.Field()
    house_num = scrapy.Field()
    house_price = scrapy.Field()
    house_style = scrapy.Field()
    house_tingshi = scrapy.Field()
    house_size = scrapy.Field()
    house_direction = scrapy.Field()
    house_imgdir = scrapy.Field()