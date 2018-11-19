## Python 实战练习##
Keys：https://github.com/Show-Me-the-Code/python
---------------------------------------------------------------------------------------------------
 
**第 0000 题：** 将你的 QQ 头像（或者微博头像）右上角加上红色的数字，类似于微信未读信息数量那种提示效果。
类似于图中效果

![头像](http://i.imgur.com/sg2dkuY.png?1)

**第 0004 题：** 任一个英文的纯文本文件，统计其中的单词出现的个数。

**第 0005 题：** 你有一个目录，装了很多照片，把它们的尺寸变成都不大于 iPhone5 分辨率的大小。

**第 0007 题：** 有个目录，里面是你自己写过的程序，统计一下你写过多少行代码。包括空行和注释，但是要分别列出来。

**第 0008 题：** 一个HTML文件，找出里面的**正文**。

**第 0009 题：** 一个HTML文件，找出里面的**链接**。

**第 0010 题：** 使用 Python 生成类似于下图中的**字母验证码图片**

![字母验证码](http://i.imgur.com/aVhbegV.jpg)

- [阅读资料](http://stackoverflow.com/questions/2823316/generate-a-random-letter-in-python) 

**第 0011 题：** 敏感词文本文件 filtered_words.txt，里面的内容为以下内容，当用户输入敏感词语时，则打印出 Freedom，否则打印出 Human Rights。

    北京
    程序员
    公务员
    领导
    牛比
    牛逼
    你娘
    你妈
    love
    sex
	jiangge
	
**第 0012 题：** 敏感词文本文件 filtered_words.txt，里面的内容 和 0011题一样，当用户输入敏感词语，则用 星号 * 替换，例如当用户输入「北京是个好城市」，则变成「**是个好城市」。

**第 0013 题：** 用 Python 写一个爬图片的程序，爬 [这个链接里的日本妹子图片 :-)](http://tieba.baidu.com/p/2166231880)

- [参考代码](http://www.v2ex.com/t/61686 "参考代码")

**第 0020 题：** [登陆中国联通网上营业厅](http://iservice.10010.com/index_.html) 后选择「自助服务」 --> 「详单查询」，然后选择你要查询的时间段，点击「查询」按钮，查询结果页面的最下方，点击「导出」，就会生成类似于 2014年10月01日～2014年10月31日通话详单.xls 文件。写代码，对每月通话时间做个统计。

**第 0021 题：** 通常，登陆某个网站或者 APP，需要使用用户名和密码。密码是如何加密后存储起来的呢？请使用 Python 对密码加密。

- 阅读资料 [用户密码的存储与 Python 示例](http://zhuoqiang.me/password-storage-and-python-example.html)

- 阅读资料 [Hashing Strings with Python](http://www.pythoncentral.io/hashing-strings-with-python/)

- 阅读资料 [Python's safest method to store and retrieve passwords from a database](http://stackoverflow.com/questions/2572099/pythons-safest-method-to-store-and-retrieve-passwords-from-a-database)


**第 0025 题：** 使用 Python 实现：对着电脑吼一声,自动打开浏览器中的默认网站。


    例如，对着笔记本电脑吼一声“百度”，浏览器自动打开百度首页。
    
    关键字：Speech to Text
    
参考思路：    
1：获取电脑录音-->WAV文件
    python record wav

2：录音文件-->文本

    STT: Speech to Text
    
    STT API Google API

3:文本-->电脑命令
