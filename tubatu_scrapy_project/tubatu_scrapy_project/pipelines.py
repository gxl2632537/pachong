# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# 定义Item Pipeline的实现，实现数据的清洗，储存，验证。
# 这里我导入是myql 我不用mogodb
import pymysql
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