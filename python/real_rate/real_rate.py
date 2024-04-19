#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: real_rate.py 
@time: 2023-10-16
@contact: danerlt001@gmail.com
@desc: 计算实际利率

银行推销一款贷款，1万元额度，每个月还利息29元，一年还款348元，银行宣传利率为3.48%, 计算实际利率和银行宣传的比例
"""
import numpy_financial as npf
from loguru import logger

logger.add("rate.log")


def calcaute_fake_rate(money, month_interest, numer=12):
    logger.info("计算虚假的年利率")
    fake_rate = (month_interest * numer) / money
    logger.info(f"{money}元额度，每月利息：{month_interest}元，虚假的年利率为：{fake_rate:.3%}")
    return fake_rate


def calcaute_real_rate(money, month_interest, number=12):
    logger.info("计算真实的年利率")
    arr = [money]
    for i in range(number):
        item = (money / number + month_interest) * -1
        arr.append(item)

    irr_for_month = npf.irr(arr)
    real_rate = pow(irr_for_month + 1, 12) - 1
    logger.info(f"{money}元额度，每月利息：{month_interest}元，真实的年利率为：{real_rate:.3%}")
    return real_rate


def main():
    money = 10000  # 贷款额度
    month_interest = 29  # 每月利息
    fake_rate = calcaute_fake_rate(money, month_interest)
    real_rate = calcaute_real_rate(money, month_interest)
    percent = real_rate / fake_rate
    logger.info(f"真实年利率是虚假年利率的{percent:.3}倍")


if __name__ == '__main__':
    main()
