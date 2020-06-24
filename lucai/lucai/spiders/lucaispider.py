# -*- coding: utf-8 -*-
import scrapy
from lucai.items import LucaiItem
import json
class LucaispiderSpider(scrapy.Spider):
    name = 'lucaispider'
    allowed_domains = []
    start_urls = ['http://m.wyz888.com/companynews.html?pagesize=20&p=1']

    def parse(self, response):
        # 当前页面所展示的li
        list_arr = response.xpath("//ul[@class='textlist']/li")
        # 遍历当前的li
        for item in list_arr:
            # 定义一个字典用于存储当前的名称和详情页的url
            list_info = {}
            list_info['title'] = item.xpath("./a/text()").extract_first()
            list_info['time'] = item.xpath("./span/text()").extract_first()
            list_info['xq_url'] = "http://m.wyz888.com" + item.xpath("./a/@href").extract_first()
            yield scrapy.Request(url= list_info['xq_url'],dont_filter=True,callback=self.handles_xq,meta=list_info)


       # 翻页
       #  if response.xpath("//div[@class='page']/a[@class='pagedown']/@href").extract_first() != 'NULL':
       #      # 获取当前页码
       #      now_page = response.xpath("//div[@class='page']/span[@class='current']/text()").extract_first()
       #      # 在当前页码上加1在请求
       #      next_page_url = "http://m.wyz888.com/companynews.html?pagesize=20&p=%d" % (now_page+1)
       #      # 再次循环请求回 调函数为parse函数
       #      yield scrapy.Request(url=next_page_url,callback=self.parse)


     # 解析详情页
    def handles_xq(self,respones):
        # 找到内容区域

        discripts = respones.xpath("//div[@class='InfoSContent']/text()").extract_first()
        content = respones.xpath("/div[@class='InfoContent']/text()").extract_first()
        xq_img_url = respones.xpath("//div[@class='InfoContent']/p/img/@src").extract_first()
        # 使用在items.py中定义的字段，因此需要导入相应的LucaiItem包
        lucai_info = LucaiItem()
        lucai_info['title']=respones.request.meta['title']
        lucai_info['time']=respones.request.meta['time']
        lucai_info['discripts']=discripts
        lucai_info['contents']=content
        lucai_info['contents_img_url']=xq_img_url
        lucai_info['image_urls']="http://m.wyz888.com" + xq_img_url

        yield lucai_info
