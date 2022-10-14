#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: litao 
@file: t_datetime.py 
@time: 2022-10-14
@contact: Tao.Li67@geely.com
@desc: 时期时间相关
"""

import datetime


def interval_ns(start, end):
    """计算时间间隔

    :param start: 开始时间
    :param end: 结束时间
    :return: 间隔时间 单位ns
    """
    if end < start:
        start, end = end, start
    diff = end - start
    seconds = diff.total_seconds()
    print(f"the interval seconds of {start} to {end} is {seconds} ")
    return seconds * 1e9


def t_interval_ns():
    start = datetime.datetime(1582, 10, 15)
    end = datetime.datetime(1970, 1, 1)
    ns = interval_ns(start, end)
    print(ns)
    hex_ns = hex(int(ns/100))
    print(hex_ns)


if __name__ == '__main__':
    t_interval_ns()

