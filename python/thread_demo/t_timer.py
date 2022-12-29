#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@file: t_timer.py
@time: 2022-10-19
@desc:
"""
import datetime
from threading import Timer

date_format = "%Y-%m-%d %H:%M:%S"


def foo():
    seconds = 1 * 60 * 60
    timer(seconds)
    print("执行foo")
    now = datetime.datetime.now()
    print(f"执行foo time: {now.strftime(date_format)}")


def timer(seconds):
    print("执行timer")
    now = datetime.datetime.now()
    print(f"执行timer time: {now.strftime(date_format)}")
    t = Timer(seconds, foo)
    t.start()


def task():
    print("before ")
    now = datetime.datetime.now()
    print(f"start time: {now.strftime(date_format)}")
    seconds = 1 * 60 * 60
    timer(seconds)
    end = datetime.datetime.now()
    print(f"end time: {end.strftime(date_format)}")


def main():
    task()


if __name__ == '__main__':
    main()

