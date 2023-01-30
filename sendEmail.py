# !/usr/bin/env python
# -*-coding:utf-8 -*-


from email.mime.text import MIMEText
import smtplib
import sys

class Email:
    def __init__(self, from_email, Email_Pass, msg, smtp_server='smtp.chinatelecom.cn'):
        # 连接到POP3服务器:
        # self.server = poplib.POP3(pop3_server)
        self.server = smtplib.SMTP_SSL(smtp_server)
        self.server.ehlo(smtp_server)
        self.server.set_debuglevel(1)  # 打印和服务器的交互信息
        self.server.login(from_email, Email_Pass)  # 登录
        self.server.sendmail(from_email, to_email, msg.as_string())  # 发送邮件
        self.server.quit()


if __name__ == '__main__':
    # 设置发送邮箱和密码
    from_email = "yus6@chinatelecom.cn"
    Email_Pass = "3kD)qVr7%m5BYA*k"
    # 　设置收件箱
    # to_email="fanglx1@chinatelecom.cn"
    to_email = ["fanglx1@chinatelecom.cn", "kongxw1@chinatelecom.cn", 'yus6@chinatelecom.cn']
    # 设置SMTP服务器
    smtp_server = "smtp.chinatelecom.cn"
    # 构造邮件内容
    msg = MIMEText("这是正文：封装测试", "plain", "utf-8")  # 第一个参数是邮件正文内容,第二个参数表示纯文本,第三个参数表示编码格式为UTF-8
    msg["From"] = from_email
    msg["To"] = ";".join(to_email)
    msg["Subject"] = "这是主题：封装测试"

    # 发送邮件
    try:
        ema = Email(from_email, Email_Pass, msg)
    except:
        print('Error:', sys.exc_info()[1])




#
#
# # 设置发送邮箱和密码
# from_email="yus6@chinatelecom.cn"
# Email_Pass="3kD)qVr7%m5BYA*k"
# #　设置收件箱
# # to_email="fanglx1@chinatelecom.cn"
# to_email=["fanglx1@chinatelecom.cn", "kongxw1@chinatelecom.cn", 'yus6@chinatelecom.cn']
# # 设置SMTP服务器
# smtp_server="smtp.chinatelecom.cn"
# # 构造邮件内容
# msg=MIMEText("这是正文：邮件测试", "plain", "utf-8") # 第一个参数是邮件正文内容,第二个参数表示纯文本,第三个参数表示编码格式为UTF-8
# msg["From"]=from_email
# msg["To"]=";".join(to_email)
# msg["Subject"]="这是主题：邮件测试"
#
#
# # 发送邮件
# try:
#     server=smtplib.SMTP_SSL(smtp_server)  # smtp.qq.com 的端口是465或587
#     server.set_debuglevel(1)    # 打印和服务器的交互信息
#     server.login(from_email,Email_Pass)   # 登录
#     server.sendmail(from_email,to_email,msg.as_string())    # 发送邮件
#     server.quit()
# except:
#     print('Error:',sys.exc_info()[1])
