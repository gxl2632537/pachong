# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FmfilesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 专辑名称
    file_album = scrapy.Field()
    # 专辑中文件名
    file_name = scrapy.Field()
    # 专辑中文件url   MP3的地址
    file_url = scrapy.Field()
