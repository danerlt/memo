#!/usr/bin/env python  
# -*- coding:utf-8 -*-  

"""
在互联网广泛普及和快速发展的时代，信息安全被越来越多的人重视，其中账户安全是信息安全最重要的一个部分。
很多网站都会有一个账号异常登录检测和诊断机制。
当账户异常登录时，会以短信或邮件的方式将登录信息（登录的时间、地区、IP 地址等）发送给已经绑定的手机或邮箱。
登录异常其实就是登录状态的改变。
服务器会记录你最近几次登录的时间、地区、IP 地址，从而得知你常用的登录地区；
如果哪次检测到你登录的地区与常用登录地区相差非常大（说明是登录地区的改变），则认为是一次异常登录。
而短信和邮箱的发送机制我们可以认为是登录的监听者，只要登录异常一出现就自动发送信息。
"""

import datetime

from observer_v2 import Observable, Observer


class Account(Observable):

    def __init__(self):
        super().__init__()
        self.__lastest_ip = {}  # 最新的IP
        self.__lastest_region = {}  # 最新的地区

    def get_region(self, ip):
        """模拟根据IP获取地区"""
        # 由 IP 地址获取地区信息。这里只是模拟，真实项目中应该调用 IP 地址解析服务
        ip_region = {
            "1.1.1.1": "测试地区",
            "2.2.2.2": "测试地区2",
            "3.3.3.3": "测试地区3",
        }
        regin = ip_region.get(ip, "")
        return regin

    def is_change_region(self, name, region):
        """判断地区是否发生了变化"""
        # 计算本次登录与最近几次登录的地区差距
        # 这里只是简单地用字符串匹配来模拟，真实的项目中应该调用地理信息相关的服务
        latest_region = self.__lastest_region.get(name)
        return latest_region is not None and latest_region != region

    def login(self, name, ip):
        """模拟登录"""
        region = self.get_region(ip)
        if self.is_change_region(name, region):
            obj = {
                "name": name,
                "ip": ip,
                "region": region,
                "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            self.notify_observers(obj)
        self.__lastest_ip[name] = ip
        self.__lastest_region[name] = region


class SmsSender(Observer):
    def update(self, observable, obj=None):
        print(f"[短信发送] {obj['name']},您好！检测到您的账户可能登录异常。")
        print(f"最近一次登录信息：\n登录地区:{obj['region']},登录IP:{obj['ip']},登录时间:{obj['time']}\n")


class EmailSender(Observer):
    def update(self, observable, obj=None):
        print(f"[邮件发送] {obj['name']},您好！检测到您的账户可能登录异常。")
        print(f"最近一次登录信息：\n登录地区:{obj['region']},登录IP:{obj['ip']},登录时间:{obj['time']}\n")


def t_login():
    account = Account()
    account.add_observer(SmsSender())
    account.add_observer(EmailSender())
    account.login("test", "1.1.1.1")
    account.login("test", "3.3.3.3")
    account.login("test2", "2.2.2.2")
    account.login("test2", "3.3.3.3")


if __name__ == '__main__':
    t_login()