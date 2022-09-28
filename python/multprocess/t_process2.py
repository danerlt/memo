#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@file: t_process.py
@time: 2022-09-28
@desc: 多进程
"""
import math
import os
import time
from multiprocessing import Process, Queue

queue = Queue()


def gen_big_list(num=10):
    """生成大列表
    :param num, 列表的数量为10的n次方 默认为10的10次方
    """
    res = []
    for item in range(10 ** num):
        res.append(item)
    return res


def split_list(origin, sub_list_count=10):
    """将一个大的list拆成多个小的list

    :param origin: 源list
    :param sub_list_count: 子list的数量
    :return: [[sub_list], [sub_list]...]
    """

    res = []
    origin_len = len(origin)
    sub_len = math.ceil((origin_len - 1) / sub_list_count)
    start = 0
    end = sub_len
    for _ in range(sub_list_count):
        sub_list = origin[start:end]
        start = end
        end = min(end + sub_len, origin_len - 1)
        res.append(sub_list)
    return res


def product(q):
    print(f"this product, pid:{os.getpid()}")
    big_list = gen_big_list(num=6)
    sub_lists = split_list(big_list, 100)
    for sub in sub_lists:
        print(f"put data ")
        q.put(sub)
        time.sleep(0.5)


def customer(q):
    print(f"this customer, pid:{os.getpid()}")
    while True:
        item = q.get()
        print(f"get data")
        res = []
        for i in item:
            res.append(i ** 2)
        time.sleep(1)


if __name__ == '__main__':
    p1 = Process(target=product, args=(queue,))
    p1.start()

    p_list = []
    max_process = 10
    for _ in range(max_process):
        p = Process(target=customer, args=(queue,))
        p.start()
        p_list.append(p)

    for p in p_list:
        p.join()
