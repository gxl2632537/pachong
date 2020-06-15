import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


test_driver = webdriver.Chrome("D:\software\PycharmProjects\chajian\chromedriver.exe")
test_driver.maximize_window()
test_driver.get("https://www.baidu.com")
#通过Linktest方法找到了设置这个标签
above = test_driver.find_element_by_id("s-usersetting-top")
#ActionChains，test_driver当做参数传入,move_to_element，perform执行所有的操作
ActionChains(test_driver).move_to_element(above).perform()
time.sleep(5)
test_driver.quit()