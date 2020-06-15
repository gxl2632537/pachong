# 这里先不使用代理，将代理代码暂时先注释掉
import requests
from lxml import etree
# 引入多进程的queue队列模块
from multiprocessing import Queue
# 引入多线程
import threading
# 导入自定义的mysql类
from mysql import insert_data
# 写2个类一个处理分也的页码
# 处理页面类 继承多线程
class Crawl_page(threading.Thread):
    # 重写父类
    def __init__(self,thread_name,page_queue,data_queue):
        super(Crawl_page,self).__init__()
        # 线程名称
        self.thread_name = thread_name
        # 页码的队列
        self.page_queue = page_queue
        # 数据内容的队列
        self.data_queue = data_queue
        # 默认的请求头
        self.header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "PHPSESSID=bpjgql41ckekbl8v3v0a22o9o2",
            "Host": "m.wyz888.com",
            "Referer": "http://m.wyz888.com/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36"
        }
    #定义run 方法 当线程start会自动调用
    def run(self):
        #打印当前启动任务的线程名字
        print('当前启动的处理页面任务为%s'%self.thread_name)
        # 页码的内容不为空的时候继续执行
        while not page_flag:
            # Queue队列去put或者get的时候，需要设置block
            # 它默认为True，需要设置成flase
            # 当前队列里没有数据了，将会抛出异常,empty,full
            try:
                # 通过get方法，将页面取出来，get为空时候，抛异常
                page = self.page_queue.get(block=False)
                page_url ="http://m.wyz888.com/companynews.html?pagesize=20&p="+str(page)
                print('当前构造的url为%s'%page_url)
                # 设置代理，当前写在这里但是占时不使用,注意一定要用动态代理，比如阿布云或者站大爷
                # proxy ={
                #     "http": "http://H08F737BJ83Z121D:7A6B559E63F5BA46@http-dyn.abuyun.com:9020",
                #     "https": "http://H08F737BJ83Z121D:7A6B559E63F5BA46@http-dyn.abuyun.com:9020",
                # }
                # 此处我们加上了代理,requests方法请求
                # response = requests.get(url=page_url, headers=self.header, proxies=proxy)
                response = requests.get(url =page_url,headers =self.header)
                # 设置了网页编码
                # response.encoding = 'gbk'
                # 将我们请求回来的网页文本数据放到数据队列里面去
                self.data_queue.put(response.text)
            except:
                pass


# 文本处理类
class Crawl_html(threading.Thread):
    # 从页码解析过来的文本数据，需要保存到data_queue
    # 重写父类
    def __init__(self,thread_name,data_queue,lock):
        super(Crawl_html, self).__init__()
        self.thread_name = thread_name
        self.data_queue = data_queue
        # 锁，多线程写入数据是必须要用到的
        self.lock = lock

    def run(self):
        print("当前启动文本处理的任务为：%s"%self.thread_name)
        # 文本数据在队列里不为空时执行
        while not data_flag:
            try:
                # 把文本数据get 出来
                text = self.data_queue.get(block=False)
                # 相应的处理方法
                result = self.parse(text)
                # 用上with 加上锁 这里就是自动开关锁
                with self.lock:
                    # 写入数据库
                    # print(result)
                    insert_data.insert_db(result)
            except:
                pass
    def parse(self,text):
         # 如果编码没有问题将请求过来的数据丢到etree.HTML中，生成对象节点树，如果有问题则编码 response.encoding='网页的编码'
         result = etree.HTML(text)
         # 找到想要获取的数据集 用result 数据集对象下的xpath方法，用xpath语法获取,要注意单双引号
         ul_list = result.xpath("//ul[@class='textlist']/li")
         # 声明一个空列表用于存放遍历数据集的数据，要遍历的数据集ul_list 这里是每个li 而不是1个ul
         list_lucai_news = []
         # 遍历数据
         for i in ul_list:
             # 声明一个字典类型 用于构造数据
             info = {}
             # 在item 下遍历注意一定要加上 .
             # 构造数据格式 用xpath 再次进行匹配查找并赋值
             info['title'] = i.xpath("./a/@title")[0]
             # 转换成str 拼接成完整的url
             info['url'] = "http://m.wyz888.com" + str(i.xpath('./a/@href')[0])
             info['time'] = i.xpath("./span/text()")[0]
             # 将匹配好的值追加到列表中
             list_lucai_news.append(info)
         return list_lucai_news

#我们定义两个全局的flag
page_flag = False
data_flag = False
# 运行方法 不是类方法不需要self
def main():
    # 定义2个队列存放页面和存放文本数据
    page_queue =  Queue()
    data_queue =  Queue()
    # 定义一个线程锁
    lock = threading.Lock()

    # 需要将页面放入到页面队列里面去
    for page in range(20,40):
        # 通过put方法将页面放到page_queue队列里面去
        page_queue.put(page)
    # 打印一个提示信息，page_queue.qsize()返回当前队列的长度
    print('当前页面队列的总量为：%s'%page_queue.qsize())

    # 定义一个列表，包含线程名，这里就用3个线程
    crawl_oage_list = ["页面处理线程1号","页面处理线程2号","页面处理线程3号"]
    # 定义一个空列表存放开启的线程
    page_thread_list = []
    for thread_name_page  in crawl_oage_list:
        # 实例化页码线程
        thread_page = Crawl_page(thread_name_page,page_queue,data_queue)
        # 启动线程
        thread_page.start()
        # 将启动后的线程放入列表中以便后面进行关闭
        page_thread_list.append(thread_page)

    #设置3个线程处理文本数据
    parseList =["文本处理线程1号","文本处理线程2号","文本处理线程3号"]
    parse_thread_list = []
    for thread_name_parse in parseList:
        thread_parse = Crawl_html(thread_name_parse, data_queue,lock)
        thread_parse.start()
        parse_thread_list.append(thread_parse)

     # 设置线程的退出机制
    global  page_flag
    # 在page_queue 为空时 即页码已经循环取完了的时候，while就不成立
    while not page_queue.empty():
        pass
    # 为空的时候设置为true 在类中就不会执行了
    page_flag = True

    # 结束页码处理线程
    for thread_page_join in page_thread_list:
        thread_page_join.join()
        print(thread_page_join.thread_name, '处理结束')

    global data_flag
    while not data_queue.empty():
        pass
    data_flag = True
    # 全部处理结束后关闭数据库
    insert_data.close_db()
    for thread_parse_join in parse_thread_list:
        thread_parse_join.join()
        print(thread_parse_join.thread_name, "处理结束")


if __name__ == '__main__':
    # 入口函数
    main()