# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#网站，栏目，标题，发布时间，作者，内容
class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    site = scrapy.Field()
    url = scrapy.Field()
    column = scrapy.Field()
    title = scrapy.Field()
    pub_time = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
    pass
