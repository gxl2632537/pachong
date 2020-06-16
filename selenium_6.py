# 导入selenium 的webdriver 包
from selenium import webdriver
from selenium.webdriver.common.by import By
# 显示等待用包
from selenium.webdriver.support.ui import WebDriverWait
# 环境判读包
from selenium.webdriver.support import expected_conditions as EC
# lxml xpath包
from  lxml import etree
import time
# chrome 设置包 可以设置成无头访问，即不打开浏览器访问到数据
from selenium.webdriver.chrome.options import Options
from mysql_2 import insert_data

class Handel_webdriver(object):
    def __init__(self):
        # 设置浏览器模式，这里占时不进行设置
        # Chrome C是大写的
        chrome_options = Options()
        # 设置为无头
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome("D:\software\PycharmProjects\chajian\chromedriver.exe")
        self.driver.maximize_window()

    def handel_job(self):
        # 设置打开的目的地址
        self.driver.get("https://search.51job.com/list/000000,000000,0000,00,9,99,%20,2,1.html")
        # 通过WebDriverWait进行显示等待,等待搜索框是否存在 在指定的地址中0.5秒查一次，id为kwdselectid的是否存在，如果存在则进行下面操作，如果在5秒内都没查到则抛出异常
        if WebDriverWait(self.driver,5,0.5).until(EC.presence_of_all_elements_located((By.ID,'kwdselectid'))):
            # 从外部获取输入的岗位信息
            input_keyword = input('请输入要查找的信息: ')
            # 通过find_element_by_id找到搜索框的控件 send_keys发送了要查找的岗位信息
            self.driver.find_element_by_id('kwdselectid').send_keys(input_keyword)
            # 这里我自己加了选择地点，选择合肥的操作
            self.driver.find_element_by_id('work_position_input').click()
            # 这里需要设置一定的等待时间，否则浏览器没有反应过来就过去了，会导致数据查不到
            time.sleep(5)
            self.driver.find_element_by_id('work_position_click_center_right_list_category_000000_150200').click()
            time.sleep(5)
            self.driver.find_element_by_id('work_position_click_bottom_save').click()
            # 点击搜索
            time.sleep(5)
            self.driver.find_element_by_class_name("p_but").click()
            # 在5秒内判断有没有找到数据
            if WebDriverWait(self.driver,5,0.5).until(EC.presence_of_all_elements_located((By.ID,"resultList"))):
                # 查看网页源代码
                # print(self.driver.page_source)

                while True:
                    # 等待2秒
                    time.sleep(2)
                    # 处理数据并存入数据库
                    self.handel_parse(self.driver.page_source)
                    # 如果有下一页则点击下一页，则会刷新页面继续获取信息，否则退出
                    if self.driver.find_element_by_xpath("//li[@class='bk'][2]/a").text == '下一页':
                        self.driver.find_element_by_xpath("//li[@class='bk'][2]/a").click()
                    else:
                        # 关闭数据库并退出
                        insert_data.close_db()
                        break
                    # time.sleep(5)
                    self.driver.quit()


    # 处理数据操作
    def  handel_parse(self,page_source):
        # 转换成lxml 对象
        html_51job = etree.HTML(page_source)
        # 单引号双引号要注意 xpath匹配拿到数据
        all_div = html_51job.xpath("//div[@id='resultList']//div[@class='el']")
        # 定义空列表拿到的数据放到空列表里面去
        info_list = []
        for item in all_div:
            info = {}
            # 这个.非常的重要，代表我们使用的是item下的xpath语句,不要把.丢了
            # 获取数据的时候，要使用列表索引为0的数据
            info['job_name'] = item.xpath("./p/span/a/@title")[0]
            info['company_name'] = item.xpath(".//span[@class='t2']/a/@title")[0]
            # 把下面这三个字段补齐
            info['company_address'] = item.xpath(".//span[@class='t3']/text()")[0]
            # money字段可能为空，try,except来进行异常处理
            try:
                info['money'] = item.xpath(".//span[@class='t4']/text()")[0]
            except IndexError:
                info['money'] = '无数据'
            info['date'] = item.xpath(".//span[@class='t5']/text()")[0]
            info_list.append(info)
            # 导入到mysql中
            insert_data.insert_db(info_list)


test_slenium = Handel_webdriver()
test_slenium.handel_job()

