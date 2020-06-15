import time
from selenium import webdriver
#启动浏览器，启动的是chrome浏览器，注意C是大写的
# 可以在代码中指定驱动的路径
test_webdriver =  webdriver.Chrome('D:\software\PycharmProjects\chajian\chromedriver.exe')
#通过get请求的方式请求https://www.echartsjs.com/examples/
test_webdriver.get("https://www.echartsjs.com/examples/")
#浏览器最大化窗口
test_webdriver.maximize_window()
#通过一个for循环来遍历这些数据
#find_elements_by_xpath，注意，双数，方法里面传递的是xpath语句
for item in test_webdriver.find_elements_by_xpath("//h4[@class='chart-title']"):
    #获取当前节点的text
    print(item.text)
#获取当前浏览器的标题
print(test_webdriver.title)
time.sleep(5)
# 浏览器退出
test_webdriver.quit()
