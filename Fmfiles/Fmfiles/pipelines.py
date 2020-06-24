# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import os
from scrapy.pipelines.files import FilesPipeline
from Fmfiles.settings import FILES_STORE
from scrapy.exceptions import DropItem

class FmfilesPipeline(FilesPipeline):
    # 动态获取资源文件默认父目录“full”，并保存为属性
    __file_dir = None
    # def process_item(self, item, spider):
    #     return item
    def get_media_requests(self, item, info):
        file_url = item['file_url']
        yield scrapy.Request(file_url)

    def item_completed(self, results, item, info):
        # file_paths系统自带的
        file_paths = [x['path'] for ok, x in results if ok]
        if not self.__file_dir:
            self.__file_dir = file_paths[0].split('/')[0]
        if not file_paths:
            raise DropItem("Item contains no files")

        # os.rename(src,dst)  方法用于重命名文件或目录 src -- 要修改的目录名 dst -- 修改后的目录名
        os.rename(FILES_STORE + file_paths[0],
                  FILES_STORE + item['file_album'] + '/' + item['file_name'])
        return item

    def close_spider(self, spider):
        if self.__file_dir is None:
            return None
        ori_filepath = FILES_STORE + self.__file_dir
        if os.path.exists(ori_filepath):
            # os.rmdir() 方法用于删除指定路径的目录  如果文件已经存在则删除文件
            os.rmdir(ori_filepath)



