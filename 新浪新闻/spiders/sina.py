# -*- coding: utf-8 -*-
import scrapy
import os
from ..items import SinanewsItem


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide']

    def parse(self, response):
        # 所有的大类和url
        parentTitle = response.xpath('//div[@id="XX_conts"]//h3/a/text()').extract()
        parentUrls = response.xpath('//div[@id="XX_conts"]//h3/a/@href').extract()

        # 所有小类标题和url
        subTitle = response.xpath('//div[@id="XX_conts"]//ul/li/a/text()').extract()
        subUrls = response.xpath('//div[@id="XX_conts"]//ul/li/a/@href').extract()

        # 遍历所有大类
        for i in range(len(parentTitle)):
            # 指定大类的目录
            parentFileName = './Data/' + parentTitle[i]

            # 创建文件夹
            if not os.path.exists(parentFileName):
                os.makedirs(parentFileName)

            # 遍历所有的小类
            for j in range(len(subTitle)):
                # 新建一个item
                item = SinanewsItem()
                item['parentUrls'] = parentUrls[i]
                item['parentTitle'] = parentTitle[i]

                # 检查小类的url是否以大类为开头，如果是，则返回True
                if_belong = subUrls[j].startswith(item['parentUrls'])

                # 如果属于大类，构建小类的目录
                if if_belong:
                    # 构建目录
                    subFileName = parentFileName + '/' + subTitle[j]
                    # 创建小类文件夹
                    if not os.path.exists(subFileName):
                        os.makedirs(subFileName)
                    # 保存数据
                    item['subUrls'] = subUrls[j]
                    item['subTitle'] = subTitle[j]
                    item['subFileName'] = subFileName
                    yield scrapy.Request(url=item['subUrls'], callback=self.parse_second, meta={'item': item})

    def parse_second(self, response):
        items = response.meta.get('item')

        # 获取当前页面所有的a标签的链接
        sonUrls = response.xpath('//a/@href').extract()
        for i in range(len(sonUrls)):
            # 检查每个链接是否是以当前大类为开头，以.shtml为结尾
            if_belong = sonUrls[i].endswith('.shtml') and sonUrls[i].replace('https', 'http').startswith(
                items['parentUrls'])
            if if_belong:
                item = SinanewsItem()
                item['parentTitle'] = items['parentTitle']
                item['parentUrls'] = items['parentUrls']
                item['subFileName'] = items['subFileName']
                item['subUrls'] = items['subUrls']
                item['subTitle'] = items['subTitle']
                item['sonUrls'] = sonUrls[i]
                yield scrapy.Request(url=item['sonUrls'], callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        # 拿到item
        item = response.meta.get('item')

        head = response.xpath('//h1[contains(@class,"main-title") or contains(@id,"artibodyTitle")]').extract_first()
        if not head:
            return
        content = response.xpath('//div[@id="artibody"]').xpath('string(.)').extract_first()
        item['head'] = head
        item['content'] = content if content else 'null'
        yield item
        # head = response.xpath('//h1[@class="main-title"]')
