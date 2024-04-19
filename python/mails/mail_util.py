#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt
@file: mail_util.py
@time: 2022-12-30
@contact: danerlt001@gmail.com
@desc: 发送邮件
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from logutil import create_logger

EMAIL_CONFIG = {}

logger = create_logger("email")


class MyEmail(object):
    def __init__(self, **kwargs):
        self.server_host = kwargs.get("server_host")
        self.server_port = int(kwargs.get("server_port"))
        self.server_username = kwargs.get("server_username")
        self.server_password = kwargs.get("server_password")
        self.sender = kwargs.get("sender")
        self.receivers = kwargs.get("receivers")


def send_mail(subject, mail_content):
    """发送邮件 QQ邮箱
    
    :param subject:  邮件主题
    :param mail_content: 邮件内容
    :return: 
    """
    try:
        email = MyEmail(**EMAIL_CONFIG)
        mm = MIMEMultipart('related')
        mm['subject'] = Header(subject, 'utf-8')
        message_text = MIMEText(mail_content, 'plain', 'utf-8')
        message_text["Subject"] = subject
        smtp_server = smtplib.SMTP_SSL(email.server_host, email.server_port)
        smtp_server.ehlo()
        smtp_server.login(email.server_username, email.server_password)
        smtp_server.sendmail(email.sender, email.receivers, message_text.as_string())
        smtp_server.close()
        logger.info("发送邮件成功!")
    except Exception as e:
        logger.exception(f"发送邮件失败, error: {e}")
        raise e


def send_outlook_mail(subject, mail_content):
    """发送outlook邮件

    :param subject:  邮件主题
    :param mail_content: 邮件内容
    :return:
    """
    try:
        email = MyEmail(**EMAIL_CONFIG)
        mm = MIMEMultipart('related')
        mm['subject'] = Header(subject, 'utf-8')
        message_text = MIMEText(mail_content, 'plain', 'utf-8')
        message_text["Subject"] = subject
        smtp_server = smtplib.SMTP()
        smtp_server.connect(email.server_host, email.server_port)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(email.server_username, email.server_password)
        smtp_server.sendmail(email.sender, email.receivers, message_text.as_string())
        smtp_server.close()
        logger.info("发送邮件成功!")
    except Exception as e:
        logger.exception(f"发送邮件失败, error: {e}")
        raise e
