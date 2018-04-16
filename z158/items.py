# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Z158Item(scrapy.Item):
	name = scrapy.Field()#资源名称
	#belong = scrapy.Field()#资源属性
	src = scrapy.Field()#资源地址
	#info = scrapy.Field()#资源介绍
    # define the fields for your item here like:
    # name = scrapy.Field()
    
