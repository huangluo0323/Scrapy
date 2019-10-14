# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import time
import os
import scrapy
from .settings import IMAGES_STORE
from scrapy.pipelines.images import ImagesPipeline


class YxlmPipeline(object):
    def process_item(self, item, spider):
        return item


class LOLImagePipeline(ImagesPipeline):
    # 发送图片请求
    def get_media_requests(self, item, info):
        image_url = item['imageLink']
        yield scrapy.Request(url=image_url)

    def item_completed(self, results, item, info):
        print(results)
        print('------------------------------------')
        # 获取到默认的path
        img_path = [x['path'] for ok, x in results if ok][0]
        # 获取默认保存的地址
        old_path = IMAGES_STORE + img_path
        # 创建文件夹
        hero_dir = IMAGES_STORE + item['heroName'] + '/'
        # 如果文件夹不存在，则创建文件夹
        if not os.path.exists(hero_dir):
            os.makedirs(hero_dir)
        # 新的图片路径
        new_path = hero_dir + item['skinName'] + '.jpg'
        try:
            os.rename(old_path, new_path)
        except:
            print('保存失败')
        return item
