# 在发送请求的时候，是必须要导入requests包的
import requests
# 通过get方法来请求数据，requests.get 参数url 是网址
# response = requests.get(url="http://www.qq.com")
# # 查看返回text
# print(response.text)
# 构造发送的数据，字典的格式
# data = {'name':'icp'}
# # post 请求 data是数据
# response=requests.post(url="http://httpbin.org/post",data=data)
# print(response.text)

# 构造的url的数据，一定要和post请求做好区分
# data ={'key1':'123','key2':456}
# response =requests.get(url="http://httpbin.org/post",params=data)
# # 查看哪个url返回的数据
# print(response.url)
# # 查看返回头
# print(response.headers)
# # 查看返回体
# print(response.text)

# 请求图片
# 一定要用wb模式
# response = requests.get(url="https://www.imooc.com/static/img/index/logo.png")
# with open('logo1.png','wb') as f:
#     # 不是返回text文本了，而是返回一个二进制的数据content
#     f.write(response.content)

# 请求的json 数据
# 定义了一个变量,设置了一个浏览器的请求头,user-agent
# header = {
#     'user-agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
# }
# response = requests.get('http://httpbin.org/ip',headers=header)
# # 查看状态码
# print(response.status_code)
# # 返回json数据，response.json
# data = response.json()
# print(data)
# print(data['origin'])

# 设置关键字tiemout 超出时间，如果超过了设定的时间没有得到返回数据 则会timeout的报错，一般项目里2-3秒比较合适
# response = requests.get(url="http://www.github.com",timeout=2)
# print(response.status_code)
# print(response.text)

# 定制请求头
# url = 'https://www.baidu.com'
# header = {
#     'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
#
# }
# response = requests.get(url=url,headers= header)
# # cookie 是一个对象RequestsCookieJar,行为和字典类似
# print(response.headers)
# print(response.cookies)
# print(response.cookies['BIDUPSID'])

# 可以查看当前发送cookie的url,可以进行测试
# url = 'http://httpbin.org/cookies'
# # 使用了字典来构造cookie
# cookies = dict(cookies_are = 'hello')
# # get方法的cookies的变量也叫cookies,不要搞混
# response = requests.get(url=url,cookies=cookies)
# print(response.text)