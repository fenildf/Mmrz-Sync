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

fr = open("mailInfo.json", "rb")
mailInfo = json.loads(fr.read())
fr.close()

def send_mail():
    smtp = SMTP_SSL(mailInfo["hostname"].encode("utf-8"))
    smtp.set_debuglevel(0)
    smtp.ehlo(mailInfo["hostname"].encode("utf-8"))
    smtp.login(mailInfo["username"].encode("utf-8"), mailInfo["password"].encode("utf-8"))
    
    msg = MIMEText(mailInfo["mailtext"], "plain", mailInfo["mailencoding"].encode("utf-8"))
    msg["Subject"] = Header(mailInfo["mailsubject"].encode("utf-8"), mailInfo["mailencoding"].encode("utf-8"))
    msg["from"] = mailInfo["from"].encode("utf-8")
    msg["to"] = mailInfo["to"].encode("utf-8")
    smtp.sendmail(mailInfo["from"].encode("utf-8"), mailInfo["to"].encode("utf-8"), msg.as_string())
    
    smtp.quit()
        
if __name__ == '__main__':
    send_mail()

