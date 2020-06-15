from selenium import webdriver
import time
test_webdriver = webdriver.Chrome("D:\software\PycharmProjects\chajian\chromedriver.exe")
test_webdriver.maximize_window()
test_webdriver.get("https://www.baidu.com")
#找到百度首页上的搜索框，发送卤三国
test_webdriver.find_element_by_xpath("//input[@id='kw']").send_keys("卤三国")
#找到百度一下这个按钮，点击一下
test_webdriver.find_element_by_xpath("//input[@id='su']").click()
time.sleep(5)
print(test_webdriver.title)
# 获取当前页面的源代码
print(test_webdriver.page_source)
#获取当前的cookie
print(test_webdriver.get_cookies())
test_webdriver.quit()