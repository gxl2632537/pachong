import requests
url = "https://www.baidu.com"
response = requests.get(url=url,verify=False)
response.encoding = 'utt-8'
print(response.text)