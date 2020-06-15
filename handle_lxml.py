# 导入lxml库 etree
from lxml import etree

# 准备的html数据，不完整。html.body，li 不完整
html_data = '''
<div>
  <ul>
       <li class="item-0"><a href="link1.html">first item</a></li>
       <li class="item-1"><a href="link2.html">second item</a></li>
       <li class="item-inactive"><a href="link3.html"><span class="bold">third item</span></a></li>
       <li class="item-1"><a href="link4.html">fourth item</a></li>
       <li class="item-0"><a href="link5.html">fifth item</a>
   </ul>
</div>
'''
# 使用etree.HTML 会自动补全里面不完整的标签

html = etree.HTML(html_data)
# 转换成字符串形式，并且解码
# print(etree.tostring(html).decode())
# print(type(html))
#使用的是双斜杠,返回是一个列表，每一个元素都是element类型,列表里面的每一个element类型的元素就
#代表我们获取到的标签元素
# 使用xpath方法获取对应的标签值 返回的是一个列表
# result = html.xpath("//li/a/text()")
# print(result)
# 获取li标签下面所有的class属性值
# result = html.xpath("//li/@class")
# print(result)
#获取的li标签href值为link1.html这个a标签,使用了单引号，如果外面使用的是
#双引号，内部一定要使用单引号,大家一定要注意
# result = html.xpath("//li/a[@href='link1.html']/text()")
# print(result)
# 我们需要获取span标签，一定要注意span他是a标签的子元素,而不是li标签的子元素,使用双斜杠
# result = html.xpath("//li//span/text()")
# print(result)
# 我们使用了last()函数，最后一个标签，-1代表倒数第二个标签
result = html.xpath("//li[last()]/a/@href")
print(result)