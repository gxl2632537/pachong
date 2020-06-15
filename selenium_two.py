import time
from selenium import webdriver

test_webdriver = webdriver.Chrome("D:\software\PycharmProjects\chajian\chromedriver.exe")

test_webdriver.get("http://www.sanguojt.com/#/")

test_webdriver.maximize_window()

for item in test_webdriver.find_elements_by_xpath('//div/div[@class="sg-header-container"]'):
    print(item.text)
time.sleep(5)
test_webdriver.quit()
