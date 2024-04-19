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
    start_date = "2023-06"  # 起始日期
    start_year, start_month = [int(x) for x in start_date.split("-")]  # 解析年月

    months = (start_year - 2023) * 12 + start_month - 1  # 计算起始月份的总月数

    idx = 1
    while balance > month_money:
        balance = balance + month_money - month_pay
        year = 2023 + months // 12  # 计算年份
        month = months % 12 + 1  # 计算月份
        month_str = f"{year:04d}-{month:02d}"  # 调整格式
        print(f"第{idx}个月 {month_str} 余额为: {balance:.2f}")

        idx += 1
        months += 1

    print("余额不足！")


def main():
    balance = 61896.09
    # 月供
    month_pay = 4706
    # 每月缴纳公积金
    month_money = 2660
    calculate(balance=balance, month_pay=month_pay, month_money=month_money)


if __name__ == '__main__':
    main()
