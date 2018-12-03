#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText

from email.header import Header

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from_addr   = '1536854522@qq.com'#邮箱账号
password = 'pntxjiquknavffdf'#第三方程序以授权码登录
smtp_server = 'smtp.qq.com' #SMTP服务器地址
to_addr     = '1536854522@qq.com'#收件人地址 

#构造MIMEText对象时，第一个参数是邮件正文，
#第二个参数是MIME的subtype,最后一个是编码方式。
#msg = MIMEText('Hello,你好！', 'plain', 'utf-8')

'''以下语句实现发送HTML格式的邮件,注意参数的不同
with open("test.html",'r',encoding='utf-8') as fp:
	contents = fp.read()
msg = MIMEText(contents, 'html', 'utf-8')
'''

'''以下语句实现发送带附件的邮件,构造MIMEMultipart对象
正文文本为MIMEText对象，附件为MIMEBase对象，均使用attach
方法添加到MIMEMultipart中。附件被读取后
'''
msg = MIMEMultipart()
msg.attach(MIMEText('Attachment Test', 'plain', 'utf-8'))

msg['From'] = from_addr
msg['Subject'] = Header(u'测试', 'utf8').encode()
msg['To'] = to_addr
'''若不在MIMEText对象中添加收（发）件人、主题等属性
则这些信息无法通过SMTP协议发给邮件传输代理(MTA)，
而是包含在发给MTA的文本中。注意：这里使用了糖衣语法'''

def add_attachment(file):
    with open(file, 'rb') as f:
        # 设置附件的MIME类型和文件名，application/octect-string:
        mime = MIMEBase('application', 'octect-string', filename=file)
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename=file)
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码对附件内容进行编码:
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)

#批量添加附件
files = ['att1.jpg','att2.jpg']
for x in files:
    add_attachment(x)




server = smtplib.SMTP(smtp_server, 25) #SMTP协议默认端口是25
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
'''sendmail第一个参数是发件邮箱，第二个参数是收件人
邮箱，是一个列表，因此可以同时发给多个人，as_string
把MIMEText或Multipart对象格式化成便于邮件发送的字符串
'''

'''MIME意为多功能Internet邮件扩展，它设计的最初目的是
为了在发送电子邮件时附加多媒体数据，让邮件客户程序能
根据其类型进行处理。在HTTP中，MIME Type类型被定义在
Content-Type header中。每个MIME类型由3部分组成：
Content-Type: [type]/[subtype]。前者是数据大类别，
后者定义具体的种类 '''

