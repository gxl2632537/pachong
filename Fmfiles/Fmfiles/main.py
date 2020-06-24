from scrapy.cmdline import execute
if __name__ == '__main__':
    # 在此添加专辑url列表或在命令行执行scrapy crawl fmfiles -a urls={多个专辑url，以逗号隔开}
   # 要爬取的专辑页
    album_urls = ['http://www.ximalaya.com/1000202/album/2667276/']
    # urls为爬虫所需外部参数的键值，与爬虫初始化器中属性名一致。这里的urls会在爬虫中获取到
    urls = ','.join(album_urls)
    execute_str = 'scrapy crawl fmfiles -a urls=' + urls
    execute(execute_str.split())
