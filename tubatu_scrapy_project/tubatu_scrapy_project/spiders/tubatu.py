# -*- coding: utf-8 -*-
# 爬虫文件 在spider文件夹中用scrapy genspider 文件名 要爬取的网址 生成的
# 这里是蜘蛛文件，用来发送请求和解析html数据的
import scrapy
import re
import json
from tubatu_scrapy_project.items import TubatuScrapyProjectItem
class TubatuSpider(scrapy.Spider):
    # 名称不能冲突，也就是说不能重复，name不能重复
    name = 'tubatu' # 爬虫项目名称
    # 允许爬虫去抓取的域名 这里一般写顶级域名
    allowed_domains = ['xiaoguotu.to8to.com'] # 允许爬取的网址
    # 项目启动之后要爬取的地址url
    start_urls = ['https://xiaoguotu.to8to.com/tuce/p_1.html'] # 从哪个网页开始爬取
    # 默认的解析方法
    def parse(self, response):
        # 打印请求头
        # print(response.request.headers)
        # 这里使用了正则表达式来获取项目的id,需要使用转义字符来转义这个. 这里的id值就是异步请求过来的，也是详情页的地址id.html
        content_id_search = re.compile(r"(\d+)\.html")  # 使用正则提取url地址，以备从中获取id
        # response后面可以直接使用xpath方法
        # response就是一个Html对象 不在需要用lxml的etree来实例化了
        pic_item_list = response.xpath("//div[@class='item']")   # 获取页面上的所有信息块
        # xpath对象返回的是一个列表 ，所以可以来遍历一下
        # print(pic_item_list)
        for item in pic_item_list:
            # 定义一个空字典
            info = {}
            # 我们可以通过extract_first这个方法来获取项目的名称,项目的数据
            # 获取的项目的名称
            # info中的名称是在items.py中定义的
            # extract(): 这个方法返回的是一个数组list，，里面包含了多个string，如果只有一个string，则返回['ABC']这样的形式。
            # extract_first()：这个方法返回的是一个string字符串，是list数组里面的第一个字符串。
            info['content_name'] = item.xpath(".//div/a/text()").extract_first() # 获取项目的名称
            # print(info['content_name'])
            # 项目的URL 即列表中图片点击进去后的url 拼接上https 形成完整的urL
            content_url = 'https:' + str(item.xpath(".//div/a/@href").extract_first())  # 获取项目的url  该url地址包含id的信息，且该id有用处，所以需要在前面使用正则来提取
            # print(content_url)
            # 根据正则找到id ,id.html就是详情页的html地址
            # 判断不为空的情况下提取否则 group()会报错
            info['content_id'] = ''
            if content_id_search.search(content_url) != None:
                info['content_id'] = content_id_search.search(content_url).group(1)  # 使用正则提取id

            # 拼接出完整的返回数据的url  即异步接口返回数据的url 在这个url 中可以看到请求后返回的很多数据 如：https://xiaoguotu.to8to.com/case/list?a2=0&a12=&a11=3552056&a6=&a3=&a10=1  在浏览器开发者模式中可以看的数据都是从这里来的
            info['content_ajax_url'] = 'https://xiaoguotu.to8to.com/case/list?a2=0&a12=&a11=' + str(info['content_id']) + '&a1=0&a17=1'
            # 我们使用yield 来发送一个异步请求，如果只想发送一次可以在for循环外面加上break 来结束发送
            # yield是一个常用于python函数定义中的关键字，它的作用是返回一个可以用来迭代（for循环）的生成器，它的应用场景通常为一个需要返回一系列值的，含有循环的函数中。
            # 使用的是scrapy.Request发送请求的
            # 回调函数,只写方法的名称，不要调用方法
            # print(info['content_ajax_url'])
            # mete=info 是把回调中需要的数据传进去，meta必须是一个字典，在下一个函数中可以使用response.meta防问
            yield scrapy.Request(url=info['content_ajax_url'],callback=self.handle_pic_parse,meta=info)   # 使用yield来发送异步请求  # 使用scrapy.Request()来发送请求，传递两个参数，其中callback(回调函数)，只写方法的名称即可

            # 页码逻辑 获取网页的页码，判断是否存在下一页
            # if response.xpath("//a[@id='nextpageid']"):
            #     # 用xpath语法获取当前页面，并使用extract_first()获取，再用int()进行转型。并将当前页码数+1得到下一页的url地址
            #     now_page = int(response.xpath("//div[@class='pages']/strong/text()").extract_first())
            #     next_page_url = 'https://xiaoguotu.to8to.com/tuce/p_%d.html' % (now_page + 1)
            #     # 再次使用yield方法，url地址为下一页的url，回调函数为parse函数
            #     yield scrapy.Request(url=next_page_url, callback=self.parse)
    # scrapy.Request 的回调函数 response是请求的返回值
    def  handle_pic_parse(self,response):
         # print(response.text) #返回的是json格式
         pic_dict_data = json.loads(response.text)['dataImg'] # json.loads()方法将json格式数据转换为字典
         for pic_item in pic_dict_data:
                for item in pic_item['album']:
                    # 使用在items.py中定义的字段，因此需要导入相应的TubatuScrapyProjectItem包
                    tubatu_info = TubatuScrapyProjectItem()
                     # 昵称
                    tubatu_info['nick_name'] = item['l']['n'] # 上传图片人的昵称
                    # 图片的地址
                    # tubatu_info['pic_url'] = 'https://pic1.to8to.com/case/'+item['l']['s']  # 图片的url地址


                    # 必须要使用这个字段，后面的数据要改成列表格式 在items中定义image_urls这个字段名称  这是将图片下载下来使用的
                    tubatu_info['image_urls'] = ['https://pic1.to8to.com/case/' + item['l']['s']]   #在items中定义image_urls这个字段名称  这是将图片下载下来使用的 下载图片则把原来的注释掉，把数据库暂时关闭
                    # 图片的名称
                    tubatu_info['pic_name'] = item['l']['t']  # 图片名称
                    tubatu_info['content_name'] = response.request.meta['content_name']
                    # print(tubatu_info['content_name'])
                    tubatu_info['content_id'] = response.request.meta['content_id']
                    tubatu_info['content_url'] = response.request.meta['content_ajax_url']
                    # yield到pipelines中用于存储，我们通过setting里面启用，如果不启用，是无法使用的  而且需要在settings.py文件中对pipelines的设置项进行打开
                    yield tubatu_info
