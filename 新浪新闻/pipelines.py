# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class SinanewsPipeline(object):
    def process_item(self, item, spider):
        # 拿到链接
        sonUrl = item['sonUrls']
        # 'http://fo.sina.com.cn/culture/tea/2018-10-22/doc-ifxeuwws6826959.shtml'
        # 'https://finance.sina.com.cn/stock/marketresearch/2019-09-27/doc-iicezzrq8687089.shtml'
        # 构建要保存的文件名
        fileName = sonUrl[10:-6].replace('/', '_')
        fileName += '.txt'
        # 打开文件并写入数据
        with open(item['subFileName'] + '/' + fileName, 'w', encoding='utf-8') as f:
            f.write(item['content'])
        return item
