# -*- coding: utf-8 -*-
import scrapy


class ZhuhuspidersSpider(scrapy.Spider):
    name = 'zhuhuspiders'
    allowed_domains = ['zhuhu.com']
    start_urls = ['http://zhuhu.com/']

    def parse(self, response):
        pass
