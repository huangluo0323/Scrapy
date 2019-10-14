# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WzrySkinItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    img_url = scrapy.Field()
    skin_name = scrapy.Field()
    hero_id = scrapy.Field()
