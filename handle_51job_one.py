import requests
from lxml import etree
import json

#使我们要请求的URL，地点为北京，岗位包含python的所有岗位,第一页数据
url = 'https://search.51job.com/list/010000,000000,0000,00,9,99,python,2,1.html'
# 设置请求头
header = {
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
"Cookie":"guid=f4ce64c6775a11dbf36cb91ac2fc6c5e; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; search=jobarea%7E%60010000%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60010000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21",
"Host":"search.51job.com",
"Sec-Fetch-Dest":"document",
"Sec-Fetch-Mode":"navigate",
"Sec-Fetch-Site":"none",
"Sec-Fetch-User":"?1",
"Upgrade-Insecure-Requests":"1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
}
# 使用get请求
response = requests.get(url=url,headers=header)
# 设置和网页一样的编码方式，否则或出现乱码
response.encoding = 'gbk'
# print(response.text)
# 使用etree.HTML()转换为lxml对象方便用xpath获取节点
# 放入requests请求过来的内容
html_51job = etree.HTML(response.text)
#单引号双引号要注意
# 获得一个数据集可以进行遍历
all_div = html_51job.xpath("//div[@id='resultList']//div[@class='el']")
# 声明一个列表
info_list = []
# 遍历
for item in all_div:
    # 声明一个字典
    info = {}
    # 这个.非常的重要，代表我们使用的是item下的xpath语句,不要把.丢了
    # 获取数据的时候，因为返回的是一个列表 要使用列表索引为0的数据 这样可以把括号去掉
    info['job_name'] = item.xpath("./p/span/a/@title")[0]
    info['company_name'] = item.xpath(".//span[@class='t2']/a/@title")[0]
    # 加入到列表中
    info_list.append(info)
# 编码：把一个Python对象编码转换成Json字符串   json.dumps()  http://json.cn/可以在线解析 一般用于存储时
# 解码：把Json格式字符串解码转换成Python对象   json.loads()
print(json.dumps(info_list))