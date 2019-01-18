# -*- coding: utf-8 -*-
"""
Created on 2019/1/18 17:22
@Author: Johnson
@Email:593956670@qq.com
@File: sendEmail.py
"""
import requests


# 发送方邮件地址
from_addr = ('*********.com')
# 授权码
password = ('********')
# 接收方邮件地址
to_addr = ('*********.com')
# smtp服务
smtp_server = ('smtp.126.com')

# 邮件对象:
msg = MIMEMultipart()
msg['From'] = _format_addr(u'***********<%s>' % from_addr)
msg['To'] = _format_addr(u'************<%s>' % to_addr)
msg['Subject'] = Header(u'************', 'utf-8').encode()
# 构建邮件文本对象
msg_text = MIMEText('html编写的发送内容', 'html', 'utf-8')
# 构建邮件图片对象
# 设置附件的MIME和文件名，这里是jpg类型:
mime = MIMEBase('image', 'jpg', filename='love.jpg')
# 加上必要的头信息:
mime.add_header('Content-Disposition', 'attachment', filename='love.jpg')
mime.add_header('Content-ID', '<0>')
mime.add_header('X-Attachment-Id', '0')
# 把附件的内容读进来:
req = requests.get(lovePhotoSrc)
mime.set_payload(req.content)
# 用Base64编码:
encoders.encode_base64(mime)

# 将邮件文本对象和邮件图片对象添加到邮件对象
msg.attach(msg_text)
msg.attach(mime)

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
