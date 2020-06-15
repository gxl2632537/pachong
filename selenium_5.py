# 导入驱动
# from selenium import webdriver
# # 简写用包
# from selenium.webdriver.common.by import By
# # 等待用包 显示等待
# from selenium.webdriver.support.ui import WebDriverWait
# # 场景判断，用来判断某个元素是否出现
# from selenium.webdriver.support import expected_conditions as EC
#
# import time
#
# test_driver = webdriver.Chrome("D:\software\PycharmProjects\chajian\chromedriver.exe")
# test_driver.maximize_window()
# test_driver.get("https://www.baidu.com")
# # WebDriverWait设置显示等待
# # 1、test_driver，2、timeout，3、轮训参数  0.5是0.5秒查找一次
# # until,EC场景判断（通过什么来找）,通过id来找相关元素
# # 每0.5查一次查不到的话到了5秒后会抛出异常 如果查到则继续执行下面的代码
# # element = WebDriverWait(test_driver,5,0.5).until(EC.presence_of_element_located((By.ID,'zhangsan')))
# element = WebDriverWait(test_driver,5,0.5).until(EC.presence_of_element_located((By.ID,'kw')))
# element.send_keys('lusanguo')
# time.sleep(5)
# test_driver.quit()

#隐式等待
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time


test_driver = webdriver.Chrome("D:\software\PycharmProjects\chajian\chromedriver.exe")
# 隐式等待 这里设置为5秒  5秒钟后没有还找到则在抛出异常
test_driver.implicitly_wait(5)
test_driver.get("https://www.baidu.com")
try:
    # test_driver.find_element_by_id('kw').send_keys('python')
    test_driver.find_element_by_id('dazhuang').send_keys('python')
    time.sleep(2)
except NoSuchElementException as e:
    print('这里报错了')
    print(e)

test_driver.quit()