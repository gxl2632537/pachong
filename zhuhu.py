# -*- coding: utf-8 -*-
import scrapy


class ZhuhuSpider(scrapy.Spider):
    name = 'zhuhu'
    allowed_domains = ['zhuhu.com']
    start_urls = ['http://zhuhu.com/']

    def parse(self, response):
        pass
