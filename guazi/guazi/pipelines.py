# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from mysql_guazi import insert_data
class GuaziPipeline:
    def process_item(self, item, spider):
        list_arr = []
        list_arr.append(item)
        insert_data.insert_db(list_arr)
        return item
