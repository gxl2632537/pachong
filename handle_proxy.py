import requests
proxy = {
    "http":'139.199.153.25:1080',
}
url = 'http://httpbin.org/ip'
for i in range(5):
# 这里设置了代理的关键字proxies
    response = requests.get(url=url,proxies=proxy)
    print(response.text)
