#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@file: t_thread_pool.py
@time: 2022-09-28
@desc: 线程池
"""
import datetime
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def foo(num):
    """模拟io请求"""
    time.sleep(1)
    t = threading.currentThread()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"time: {now} 模拟IO请求, pid: {os.getpid()}, thread_id: {t.ident}")
    res = num * 2
    return res


def main():
    max_thread = 10
    name_list = [i for i in range(10)]
    all_task = []
    with ThreadPoolExecutor(max_workers=max_thread) as pool:
        for name in name_list:
            task = pool.submit(foo, name)
            all_task.append(task)

    for feture in as_completed(all_task):
        res = feture.result()
        print(res)


if __name__ == '__main__':
    main()
