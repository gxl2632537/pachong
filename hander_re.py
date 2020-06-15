# 导入正则表达式模块
# -*- coding: UTF-8 -*-
import re
# 用这个正则来匹配数字
# pattern = re.compile(r'\d+')
# # match 从头部开始匹配，如果匹配失败了则返回none
# m1 = pattern.match('one12twothree34four')
# print(m1)
# # 因为是从头部开始找的，所以没有找到自己返回none
# # match 指定起始位置为终止位置进行查找
# m2 = pattern.match('one12twothree34four',3,10)
# # 查看数据可以使用group()方法
# print(m2.group())
###########################################
# search()方法在字符串任意位置进行匹配，match是从头匹配
# m1 = pattern.search("one12twothree34four")
# print(m1.group())
########################################
# findall方法，搜索全文，查到的话返回一个符合正则的列表，查不到则返回一个空列表
# result = pattern.findall("one12twothree34four")
# print(result)
# split()将字符串按照一定的方式进行分割 在正则中也可以分割成一个列表
# string = "a,b,c"
# str1 = string.split(',')
# print(str1)
# string = 'a,b;; c  d'
# pattern = re.compile(r'[\,\;\s]+')
# # 以正则的方式分割字符串，需要将字符串传入正则对象的split方法中去
# m3 = pattern.split(string)
# print(m3)
#####################
# string = '<h1 class="test">imooc</h1>'
# # 用sub 方法将字符串的1换成2
# pattern = re.compile(r"\d")
# # sub()第一个参数是要符合正则的换成什么，第二个参数是在哪里换
# m4 = pattern.sub('2',string)
# print(m4)
# sub()第三参数是count 是指定要替换的次数，如果不指定则全部替换
# pattern = re.compile('\d')
# m5 = pattern.sub('2',string,1)
# print(m5)

# print(pattern.sub('2',string,1))
#分组乱入，使用了search方法来获取分组里面的数据，通过group()里面的数字，来
#确定分组,这个正则表达式，也在函数中用到了
#.\d被后面的\1所引用,使用了命名分组方法，制定了一个名字，classname

# pattern = re.compile('<(.\d)\sclass="(?P<classname>.*?)">.*?</(\\1)>')

# print(pattern.search(string).group(1))
# 定义一个函数,match对象
# def func(m):
#     return 'after sub' + m.group('classname')
#
# print(pattern.sub(func,string))

# string = '<h1 class="test">imooc</h1>'
# # 使用贪婪模式匹配所有字符
# pattern1 = re.compile('<.\d\sclass=.*>')
# print(pattern1.search(string).group())
# # 使用非贪婪模式匹配数据
# pattern2 = re.compile('<.\d\sclass=".*?>')
# print(pattern2.search(string).group())

# 考题

# s = "<div><p>岗位职责：</p><p>完成推荐算法、数据统计、接口、后台等服务器端相关工作</p><p><br></p><p>必备要求：</p><p>良好的自我驱动力和职业素养，工作积极主动、结果导向</p><p>&nbsp;<br></p><p>技术要求：</p><p>1、一年以上 Python 开发经验，掌握面向对象分析和设计，了解设计模式</p><p>2、掌握HTTP协议，熟悉MVC、MVVM等概念以及相关WEB开发框架</p><p>3、掌握关系数据库开发设计，掌握 SQL，熟练使用 MySQL/PostgreSQL 中的一种<br></p><p>4、掌握NoSQL、MQ，熟练使用对应技术解决方案</p><p>5、熟悉 Javascript/CSS/HTML5，JQuery、React、Vue.js</p><p>&nbsp;<br></p><p>加分项：</p><p>大数据，数理统计，机器学习，sklearn，高性能，大并发。</p></div>"
# 导入re模块，写正则表达式，使用sub方法将所有的标签，都替换为空

# pattern = re.compile('[<div>|<p>|</p>|</div>|<br>|&nbsp;]')
# s1 = pattern.sub('',s)
# print(s1)