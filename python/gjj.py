#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
"""
@desc: 公积金计算 
"""

import datetime


def calculate(balance=0, month_pay=0, month_money=0):
    """

    :param balance: 公积金余额
    :param month_pay: 月供
    :param month_money: 每月缴纳公积金
    :return:
    """
    now = datetime.datetime.now()
    i = 0
    while balance >= month_pay:
        balance -= month_pay
        i += 1
        print(f"还款{i}个月，余额：{balance}")
        balance += month_money


def main():
    balance = 63334.89
    # 月供
    month_pay = 4740
    # 每月缴纳公积金
    month_money = 2660
    calculate(balance=balance, month_pay=month_pay, month_money=month_money)


if __name__ == '__main__':
    main()
