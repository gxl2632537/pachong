import requests
import re
class Login(object):
        def __init__(self):
            self.request_session = requests.session()
            self.header = {
                "User - Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 83.0.4103.61Safari / 537.36"
            }
            self.csrf_value = ''

        def handel_csrf_token(self):
            self.index_url = "http://flask.zhaedu.com/mall/product/list/1"
            csrf_response = self.request_session.get(url=self.index_url, headers=self.header)
            csrf_search = re.compile(r'name="csrf_token"\stype="hidden"\svalue="(.*?)">')
            self.csrf_value = csrf_search.search(csrf_response.text).group(1)
            return self.csrf_value

        def handle_login(self):
            self.handel_csrf_token()
            username = input("请输入用户名：")
            password = input("请输入密码：")
            login_url = "http://flask.zhaedu.com/accounts/login"
            data = {
                "csrf_token":self.csrf_value,
                "username":username,
                "password":password,
            }
            self.request_session.post(url = login_url,headers =self.header,data=data)
            response = self.request_session.get(url=self.index_url)
            print(response.text)

if __name__ == "__main__":
    flask = Login()
    flask.handle_login()
