# -*- coding: utf-8 -*-
import scrapy
import os
import json
# 选择器
from scrapy.selector import Selector
from Fmfiles.items import FmfilesItem
from Fmfiles.settings import FILES_STORE


class FmfilesSpider(scrapy.Spider):
    name = 'fmfiles'
    # allowed_domains是爬虫限制域名，所有进入爬取队列的url必须符合这个域名，否则不爬取，该项目不限制
    allowed_domains = ['']
    # PC端起始url
    pc_url = 'http://www.ximalaya.com/'
    # 移动端起始url
    mobile_url = 'http://m.ximalaya.com/'
    def __init__(self, urls=None):
        super(FmfilesSpider, self).__init__()
        self.urls = urls.split(',')

    def start_requests(self):
        for url in self.urls:
            # startswith()方法用于检查字符串是否是以指定子字符串开头如果是则返回 True，否则返回 False
            if url.startswith(self.mobile_url):
                yield self.request_album_url(url)
            elif url.startswith(self.pc_url):
                yield scrapy.Request(url=url, callback=self.parse_pc)

    def request_album_url(self, album_url=''):
        if len(album_url) == 0:
            return None
        album_url = album_url.strip().strip('/')
        album_id = album_url.split('/')[-1]
        return scrapy.Request(album_url,
                              meta={'aid': album_id},
                              callback=self.parse,
                              dont_filter=True)
    def parse_pc(self, response):
        # 从PC端专辑html中解析出移动端专辑url
        mobile_url = response.xpath('//head/link[contains(@rel, "alternate")]/@href').extract_first()
        yield self.request_album_url(mobile_url)

    def parse(self, response):
        # 专辑名称
        album_name = response.xpath("//div[@class='infoWrapper sG_']/p/text()").extract_first()
        # self.album_name = album_name
        # 文件的路径+文件名
        filepath = FILES_STORE + album_name
        #不存在则创建dir dir的名字就是上面的专辑名
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        meta = response.meta
        # print(response.meta)
        yield self.json_formrequest(aname=album_name,
                                    aid=meta['aid'])

    # 其中json_formrequest函数提交资源文件json表单，表单参数为json所在url、专辑id、资源页数(一页20个文件)。
    def json_formrequest(self, aname='', aid=0, page=1):
        moreurl = '/album/more_tracks'
        # album_id = album_url.split('/')[-1]
        page = str(page)
        # 这里是请求的api 是开发者平台的
        formrequest = scrapy.FormRequest(url='http://m.ximalaya.com' + moreurl,
                                         formdata={'url': moreurl,
                                                   'aid': str(aid),
                                                   'page': str(page)},
                                         meta={'aname': str(aname),
                                               'aid': str(aid),
                                               'page': str(page)},
                                         method='GET',
                                         callback=self.parse_json,
                                         dont_filter=True)
        return formrequest

    def parse_json(self, response):
        # print(response.text)
        jsondata = json.loads(response.text)
        if jsondata['res'] is False:
            return None
        next_page = jsondata['next_page']
        selector = Selector(text=jsondata['html'])
        file_nodes = selector.xpath('//li[@class="item-block"]')
        # print(file_nodes)
        if file_nodes is None:
            return None
        meta = response.meta
        for file_node in file_nodes:
            file_name = file_node.xpath('a[1]/h4/text()').extract_first().strip()
            file_url = file_node.xpath('a[2]/@sound_url').extract_first().strip()
            item = FmfilesItem()
            item['file_album'] = meta['aname']
            item['file_name'] = file_name + '.' + file_url.split('.')[-1]
            item['file_url'] = file_url
            yield item
        if int(next_page) == 0:
            return None
        if int(next_page) == (int(meta['page']) + 1):
            yield self.json_formrequest(aname=meta['aname'],
                                        aid=meta['aid'],
                                        page=next_page)
