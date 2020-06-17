from scrapy import cmdline
# 在我们scrapy项目里面，为了方便运行scrapy的项目的这里创建一个入口文件，在这里只要运行这个文件项目就会运行了
# cmdline.execute()
# scrapy crawl 项目的名称
cmdline.execute("scrapy crawl tubatu".split())