# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SinanewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #大类的标题和url
    parentTitle = scrapy.Field()
    parentUrls= scrapy.Field()

    #小类的标题和url
    subTitle = scrapy.Field()
    subUrls = scrapy.Field()

    #小类的路径
    subFileName = scrapy.Field()
    #小类的子链接
    sonUrls = scrapy.Field()

    #文章的标题和内容
    head = scrapy.Field()
    content = scrapy.Field()


