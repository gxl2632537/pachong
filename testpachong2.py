import requests
from lxml import etree
from multiprocessing import Queue
import threading
import json
import pymysql
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
list_conetent = []
# count = 0
for i in range(15050,15052):
    response = requests.get(url='http://m.wyz888.com/companynews/'+ str(i) +'.html',headers =header)
    # print("url："+ str('http://m.wyz888.com/companynews/'+ str(i) +'.html'))
    result = etree.HTML(response.text)
    info ={}
    info['title'] =result.xpath("//div/div[@class='InfoTitle']/h1/text()")[0]
    info['info_from_wrap'] =result.xpath("//div/div[@class='info_from_wrap']/a[1]/text()")[0]
    info['infoSContent'] =result.xpath("//div/div[@class='InfoSContent']/text()")[0]
    # info['infoContent'] =result.xpath("//div/div[@class='InfoContent']/text()")
    info['infoContent'] = ''
    # 这里需要循环输出 内容是列表拼接出来的
    for it in result.xpath("//div/div[@class='InfoContent']/text()"):
        info['infoContent']= info['infoContent'] + it
    info['img'] =result.xpath('//*[@id="right"]/div[2]/div[4]/p/img/@src')[0]
    list_conetent.append(info)
    # count = count + 1
    # print(count)
    # print(info)
# print(list_conetent)
# 将抓取到的值插入到数据库
# 打开数据库
db = pymysql.connect("localhost","root","root","testpachong1")
# 使用cursor()方法获取操作游标
cursor = db.cursor()
count = 0
for item in list_conetent:
    # sql 语句动态化
    sql = "INSERT INTO test2(title,\
           info_from_wrap, infoSContent,infoContent,img) \
           VALUES ('%s', '%s','%s','%s','%s')" % \
          (item['title'], item['info_from_wrap'], item['infoSContent'], item['infoContent'] ,item['img'])
    try:
        # 执行sql
        cursor.execute(sql)
        db.commit()
        count = count + 1
        # print(count)
    except:
        # print(sql)
        db.rollback()

print("已成功插入" + str(count) + "条数据")
db.close()