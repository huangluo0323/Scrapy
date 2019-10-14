# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import YxlmItem
import time


class LolSpider(scrapy.Spider):
    name = 'lol'
    allowed_domains = ['lol.qq.com', 'game.gtimg.cn']
    start_urls = ['https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js']

    def parse(self, response):
        res = json.loads(response.text)
        for hero in res['hero']:
            hero_id = hero['heroId']
            detail_url = f'https://game.gtimg.cn/images/lol/act/img/js/hero/{hero_id}.js'
            yield scrapy.Request(url=detail_url, callback=self.parse1)

    def parse1(self, response):
        res = json.loads(response.text)
        for skin in res['skins']:
            item = YxlmItem()
            url = skin.get('mainImg', '')
            if not url:
                continue
            item['imageLink'] = url
            item['heroName'] = skin['heroName']
            item['skinName'] = skin['name']
            item['description'] = skin.get('description', 'null')
            yield item
