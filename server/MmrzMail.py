# -*- coding: utf-8 -*-

import os, sys
import smtplib
import json
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText

# Refer to: https://my.oschina.net/u/1179554/blog/214387
mailInfo = {
    "from": "发信人用户名@qq.com",
    "to": "收信人用户名@qq.com",
    "hostname": "smtp.qq.com",
    "username": "账户名",
    "password": "密码",
    "mailsubject": "邮件标题",
    "mailtext": "邮件正文",
    "mailencoding": "utf-8",
}

mail_T = """
<p>您的验证码为: {0}, 30分钟内有效. 请点击以下链接以验证, 若链接无效请拷贝至浏览器中访问</p>\
<a href='https://mmrz.zhanglintc.co/verify_email?username={1}&veriCode={0}'>\
https://mmrz.zhanglintc.co/verify_email?username={1}&veriCode={0}\
</a>\
"""

fr = open("mailInfo.json", "rb")
mailInfo = json.loads(fr.read())
fr.close()

def send_mail(
        username,
        p_veriCode,
        p_from = None,
        p_to = None,
        p_hostname = None,
        p_username = None,
        p_password = None,
        p_mailsubject = None,
        p_mailtext = None,
        p_mailencoding = None
    ):
    p_from = p_from or mailInfo["from"].encode("utf-8")
    p_to = p_to or mailInfo["to"].encode("utf-8")
    p_hostname = p_hostname or mailInfo["hostname"].encode("utf-8")
    p_username = p_username or mailInfo["username"].encode("utf-8")
    p_password = p_password or mailInfo["password"].encode("utf-8")
    p_mailsubject = p_mailsubject or mailInfo["mailsubject"].encode("utf-8")
    p_mailtext = p_mailtext or mail_T.format(p_veriCode, username)
    p_mailencoding = p_mailencoding or mailInfo["mailencoding"].encode("utf-8")

    smtp = SMTP_SSL(p_hostname)
    smtp.set_debuglevel(0)
    smtp.ehlo(p_hostname)
    smtp.login(p_username, p_password)
    
    msg = MIMEText(p_mailtext, "html", p_mailencoding)
    msg["Subject"] = Header(p_mailsubject, p_mailencoding)
    msg["from"] = p_from
    msg["to"] = p_to

    smtp.sendmail(p_from, p_to, msg.as_string())
    
    smtp.quit()
        
if __name__ == '__main__':
    # send_mail(username = "zhanglin", p_veriCode = "12312312", p_to = "i@smilebin.top")
    pass

