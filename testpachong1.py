# -*- coding: UTF-8 -*-
import requests
from lxml import etree
import json
import pymysql
# mysql的内容是我自己加的，目的是将抓取来的内容写到mysql里面
# 要抓取的单页目标url
# url = 'http://m.wyz888.com/companynews.html'
# url = 'http://m.wyz888.com/companynews.html?pagesize=20&p=2'
url = 'http://m.wyz888.com/companynews.html?pagesize=20&p=3'
# url = 'http://m.wyz888.com/companynews.html?pagesize=20&p=4'
# url = 'http://m.wyz888.com/companynews.html?pagesize=20&p=5'


#要抓取数据的请求头 要在sublime中用正则加上双引号
# find :(.*?)\:(.*?)\n
# replace :"$1":"$2",\n
header = {
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.8",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
"Cookie":"PHPSESSID=bpjgql41ckekbl8v3v0a22o9o2",
"Host":"m.wyz888.com",
"Referer":"http://m.wyz888.com/",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36"
}

# 使用get方法请求数据
response = requests.get(url=url,headers=header)
# print(response.text)
# 如果编码没有问题将请求过来的数据丢到etree.HTML中，生成对象节点树，如果有问题则编码 response.encoding='网页的编码'
result = etree.HTML(response.text)
# 找到想要获取的数据集 用result 数据集对象下的xpath方法，用xpath语法获取,要注意单双引号
ul_list = result.xpath("//ul[@class='textlist']/li")
# 声明一个空列表用于存放遍历数据集的数据，要遍历的数据集ul_list 这里是每个li 而不是1个ul
list_lucai_news = []
# 遍历数据
for i in ul_list:
    # 声明一个字典类型 用于构造数据
    info = {}
    # 在item 下遍历注意一定要加上 .
    # 构造数据格式 用xpath 再次进行匹配查找并赋值
    info['title'] = i.xpath("./a/@title")[0]
    # 转换成str 拼接成完整的url
    info['url'] ="http://m.wyz888.com" +str(i.xpath('./a/@href')[0])
    info['time'] = i.xpath("./span/text()")[0]
    # 将匹配好的值追加到列表中
    list_lucai_news.append(info)

# 用json.dumps进行编码存储，可以用json.loads()解码查看
# print(json.dumps(list_lucai_news))




# 将抓取到的值插入到数据库
# 打开数据库
db = pymysql.connect("localhost","root","root","testpachong1")
# 使用cursor()方法获取操作游标
cursor = db.cursor()
count = 0
for item in list_lucai_news:
    # sql 语句动态化
    sql = "INSERT INTO test1(name, \
           hrefurl, time) \
           VALUES ('%s', '%s','%s')" % \
          (item['title'], item['url'], item['time'])
    try:
        # 执行sql
        cursor.execute(sql)
        db.commit()
        count = count + 1
    except:
        db.rollback()
print("已成功插入" + str(count) + "条数据")
db.close()