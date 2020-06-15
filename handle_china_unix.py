# 导入3个包，requests,re正则表达式包，time 时间包
import requests
import re
import time

# 访问一个网站的url 通过get方法
index_url = 'http://account.chinaunix.net/login'

# 通过浏览器获取到的，(.*?):(.*),替换"$1":"$2",
header = {
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9",
"Connection":"keep-alive",
"Host":"account.chinaunix.net",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36",
}

# 构造一个session
login_session = requests.session()
# 构造一个token 的正则表达式
token_search = re.compile(r'name="_token"\svalue="(.*?)"')
# 一定要用login_session 否则无法保存cookie
index_response = login_session.get(url = index_url,headers = header)
# 获取token
token_value = re.search(token_search,index_response.text).group(1)
# 开始构造登陆的数据
data = {
    "username":"dazhuang_imooc",
    "password":"abcd1234",
    "_token":token_value,
    "_t":int(time.time())#他是时间戳
}

# 登陆的时候使用的接口，使用url
login_url = "http://account.chinaunix.net/login/login"
# 使用的是POST 请求
login_session.post(url =login_url,headers = header,data= data)

# 登陆后再去请求设置页面
phone_url = 'http://account.chinaunix.net/ucenter/user/index'
phone_response = login_session.get(url=phone_url,headers= header)
# 是可以看到设置页面的手机号码的
print(phone_response.text)


