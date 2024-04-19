#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@file: t_process.py
@time: 2022-09-28
@desc: 多进程
"""
import os
import time
from multiprocessing import Process, Queue

queue = Queue()


def product(q):
    print(f"this product, pid:{os.getpid()}")
    for item in range(10 ** 2):
        print(f"put data {item}")
        q.put(item)
        time.sleep(0.5)


def customer(q):
    print(f"this customer, pid:{os.getpid()}")
    while True:
        item = q.get()
        print(f"get data {item}")
        res = item ** item
        print(res)
        time.sleep(0.1)


if __name__ == '__main__':
    p1 = Process(target=product, args=(queue,))
    p1.start()

    p_list = []
    for i in range(5):
        p = Process(target=customer, args=(queue,))
        p.start()
        p_list.append(p)

    for p in p_list:
        p.join()
