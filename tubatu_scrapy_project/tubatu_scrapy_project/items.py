# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# 相当一个容器 这里定义要存储到数据库的字段名称
import scrapy


class TubatuScrapyProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #装修名称
    content_name = scrapy.Field()
    #装修id
    content_id = scrapy.Field()
    #请求url
    content_url = scrapy.Field()
    #昵称
    nick_name = scrapy.Field()
    #图片的Url
    # pic_url = scrapy.Field()
    #是必须的，必须要定义为image_urls 这是下载的图片是属性 这是固定的值不是自定义的 如果需要下载图片则需要把原来 的图片url注释掉
    image_urls = scrapy.Field()
    #图片的名称
    pic_name = scrapy.Field()
