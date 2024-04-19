#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@file: t_thread.py
@time: 2022-09-28
@desc: 线程用法
"""
import datetime
import os
import threading
import time
from threading import Thread


def foo():
    time.sleep(1)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:dddd%S")
    t = threading.current_thread()
    print(f"time: {now} 模拟IO请求, pid: {os.getpid()}, thread_id: {t.ident}")


def main():
    max_thread = 10
    threads = []
    for i in range(max_thread):
        t = Thread(target=foo)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
