import requests
#通过execjs这个包，来解析js
import execjs
import re
from mysql_3 import insert_data

#我们请求城市的接口
url = 'https://www.guazi.com/www/buy'

#cookie值要删掉，否则对方会根据这个值发现我们，并且屏蔽我们
#要通过正则表达式处理请求头,里面有空格，大家一定要注意
header = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Connection":"keep-alive",
    "Host":"www.guazi.com",
    "Referer":"https://www.guazi.com/www/buy",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36",
}

response = requests.get(url=url,headers=header)
#设置返回的编码
response.encoding = 'utf-8'
# 瓜子做了反爬虫的机制，返回的状态码是203要破解js
# print(response.status_code)
"""
1、发送的第一个请求，返回状态码是203，请求时是不带有任何信息
2、猫腻就在203返回的这个 页面里，html页面，但是，里面带有js
3、这段代码经过我们分析，他是用来设置cookie,Cookie: antipas=84381S2R54H236370l9820h6672
4、再次发送请求，要带着这个cookie，这样就能返回正常的html页面了

反爬策略方法的分析
----------------------------------------------------

破解反爬
1、先把返回数据copy出来，发现，里面数据就在js
2、 eval(function(p,a,c,k,e,r){e=function(c){return(c<62?'':e(parseInt(c/62)))+((c=c%62)>35?String.fromCharCode(c+29):c.toString(36))};if('0'.replace(0,e)==0){while(c--)r[e(c)]=k[c];k=[function(e){return r[e]||e}];e=function(){return'([efhj-pru-wzA-Y]|1\\w)'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}
3、这个叫js混淆
4、去掉eval后面的代码，都复制出来。粘贴到浏览器的开发者工具里面去
5、粘贴到console标签里,敲一下回车！！！,后面的分号别吃了
6、解析出来的是半混淆的代码，能看到相关的函数了，但是还是一大坨
7、粘贴到https://beautifier.io/，格式化
8、在Python里如何调用JS ,>pip install pyexecjs
9、破解成功了！！！
"""
# print(response.text)
if '正在打开中,请稍后' in response.text:
    #通过正则表达式获取了相关的字段和值
    value_search = re.compile(r"anti\('(.*?)','(.*?)'\);")
    string = value_search.search(response.text).group(1)
    key = value_search.search(response.text).group(2)
    #读取，我们破解的js文件
    with open('guazi.js','r',encoding='UTF-8') as f:
        f_read = f.read()
    #使用execjs包来封装这段JS,传入的是读取后的js文件
    js = execjs.compile(f_read)
    # 参数一就是js文件里的函数，参数二就是传入从参数，返回值就是执行完函数的返回值
    js_return = js.call('anti',string,key)
    cookie_value = 'antipas='+js_return
    header['Cookie'] = cookie_value
    # 设置请求的cookie 携带cookie进行请求 有返回值则成功破解js 破解瓜子的反派机制
    response_second = requests.get(url=url,headers=header)

    # print(response_second.text)

    # 找到城市的地址url
    # city_search = re.compile(r'href="\/(.*?)\/buy"\stitle=".*?">(.*?)\s+</a>')
    city_search = re.compile(r'href="\/(.*?)\/buy"\stitle="(.*?)">(.*?)<\/a>')
    # 由于瓜子更新了反爬虫机制所以现在获取不到城市了，这里我是在源代码中复制到本地的txt文件中在txt文件中进行正则查找
    with open('guazicity.txt','r',encoding='utf-8') as f :
        fileread = f.read()
        # print(re.findall(city_search,fileread))
        city_list = re.findall(city_search,fileread)
    # 找到品牌的地址url
    brand_search = re.compile(r'href="\/www\/(.*?)\/c-1/#bread"\s+>(.*?)</a>')
    # 正则进行匹配返回一个列表
    # city_list = city_search.findall(response_second.text)
    brand_list = brand_search.findall(response_second.text)
    # print(city_list)
    # 遍历城市，这里做为演示只搜索北京地区的
    # print(city_list)
    info_list = []
    for city in city_list:
        # if city[2] == '北京':
            for brand in brand_list:
                info = {}
                #https://www.guazi.com/anqing/buy
                #https://www.guazi.com/anqing/audi/#bread
                #https://www.guazi.com/anqing/audi/o1i7/#bread
                info['task_url'] = 'https://www.guazi.com/'+city[0]+'/'+brand[0]+'/'+'o1i7'
                info['city_name'] = city[1]
                info['brand_name'] = brand[1]
                info['item_type'] = 'list_item'
                info_list.append(info)
                # print(info_list)
insert_data.insert_db(info_list)
insert_data.close_db()