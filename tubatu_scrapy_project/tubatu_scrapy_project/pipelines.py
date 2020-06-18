# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# 定义Item Pipeline的实现，实现数据的清洗，储存，验证。
# 这里我导入是myql 我不用mogodb
import pymysql
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
# 实现将数据保存到mysql中去
class TubatuScrapyProjectPipeline:
    # 初始化
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(host='localhost', user='root', passwd='root',db='testpachong1')  # 后面三个依次是数据库连接名、数据库密码、数据库名称
        # get cursor
        self.cursor = self.connect.cursor()
        print("连接数据库成功")
    #     执行的操作
    def process_item(self, item, spider):
        # sql语句
        insert_sql = """
        insert into tubatu(content_name, content_id, content_url, nick_name, pic_url,pic_name) VALUES (%s,%s,%s,%s,%s,%s)
        """
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql, (item['content_name'], item['content_id'], item['content_url'], item['nick_name'],
                                         item['pic_url'],item['pic_name']))
        # 提交，不进行提交无法保存到数据库
        self.connect.commit()

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.connect.close()
#自定义的图片下载类需要继承于ImagesPipeline
class TubatuImagePipeline(ImagesPipeline):
    # def get_media_requests(self, item, info):
    #     #根据image_urls中指定的URL进行爬取
    #     pass

    # 请求下载
    def get_media_requests(self, item, info):
        # 根据image_urls中指定的url进行爬取
        for img_url in item['image_urls']:
            # 下载完后给别的函数去改名字，所以用meta传下去
            yield scrapy.Request(img_url, meta={'item': item})

    # 该方法默认即可，一般不做修改（用于下载图片）
    def item_completed(self, results, item, info):
        #图片下载完毕之后，处理结果的,返回是一个二元组
        #(success,image_info_or_failure)
        # 图片下载完成之后，处理结果的方法，返回的是一个二元组
        # 返回的格式：(success, image_info_or_failure)  第一个元素表示图片是否下载成功；第二个元素是一个字典，包含了image的信息
        image_paths = [x['path'] for ok,x in results if ok] # 通过列表生成式
        if not image_paths:
            raise DropItem('Item contains no images') # 抛出异常，图片下载失败（注意要导入DropItem模块）
        return item

    # 用于给下载的图片设置文件名称和路径
    def file_path(self, request, response=None, info=None):
        # #用于给下载的图片设置文件名称的
        # url = request.url
        # file_name = url.split('/')[-1]
        # #aaaa.jpg
        # return file_name
        item = request.meta['item']  # 从上面的get_media_requests()方法中获取到item
        folder = item['content_name']  # 获取爬取到的数据的content_name
        folder_strip = folder.strip()  # 去除空格
        image_guid = request.url.split('/')[-1]  # request.url 获取到如下的图片地址
        # 如："https://pic.to8to.com/case/2018/08/27/20180827165930-fac62168_284.jpg"
        # 拆分后为：20180827165930-fac62168_284.jpg
        filename = u'images/{}/{}'.format(folder_strip, image_guid)
        return filename
