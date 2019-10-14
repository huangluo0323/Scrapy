# -*- coding: utf-8 -*-
import scrapy
from ..items import WzrySkinItem


class WzrySpider(scrapy.Spider):
    name = 'WZRY'
    allowed_domains = ['pvp.qq.com']
    start_urls = ['https://pvp.qq.com/web201605/herolist.shtml']

    def parse(self, response):
        li_list = response.xpath('//ul[@class="herolist clearfix"]/li')
        for li in li_list:
            name = li.xpath('.//a/text()').extract_first()
            hero_url = li.xpath('.//a/@href').extract_first()
            hero_id = hero_url.replace('herodetail/','').replace('.shtml','')
            detail_url = 'https://pvp.qq.com/web201605/' + hero_url
            yield scrapy.Request(url=detail_url, callback=self.parse1, meta={'name': name,'hero_id':hero_id})

    def parse1(self, response):
        name = response.meta.get('name')
        hero_id = response.meta.get('hero_id')
        skin_names = response.xpath('.//ul[@class="pic-pf-list pic-pf-list3"]/@data-imgname').extract_first().split('|')
        for i in range(len(skin_names)+1):
            item = WzrySkinItem()
            item["img_url"] = f'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{hero_id}/{hero_id}-bigskin-{i+1}.jpg'
            item["skin_name"] = skin_names[i]
            item["name"] = name
            yield item
