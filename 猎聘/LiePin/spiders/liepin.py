# -*- coding: utf-8 -*-
import scrapy
from ..items import LiepinItem


class LiepinSpider(scrapy.Spider):
    name = 'liepin'
    allowed_domains = ['liepin.com']
    start_urls = ['https://www.liepin.com/zhaopin/?key=python']

    def parse(self, response):
        job_list = response.css('.sojob-list li')
        for li in job_list:
            item = LiepinItem()
            item['title'] = li.xpath('.//h3/a/text()').extract_first().strip()
            url = li.xpath('.//h3/a/@href').extract_first()
            item['link'] = url if url.startswith('https') else 'https://www.liepin.com' + url
            info = li.xpath('.//p/@title').extract_first().split('_')
            item['money'] = info[0]
            try:
                item['addr'] = info[1].split('-')[0]
            except Exception:
                pass
            item['xue'] = info[2]
            item['age'] = info[3]
            yield item
        next = response.xpath('//div[@class="pagerbar"]/a[last()-1]/@href').extract_first()
        next_url = 'https://www.liepin.com' + next if len(next) > 20 else ''
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse)
