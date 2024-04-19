#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: car.py
@time: 2023-04-19
@contact: danerlt001@gmail.com
@desc:
汽车将交替行驶和停放一段时间。当它开始驾驶（或停车）时，它会打印当前的模拟时间。
"""

import simpy


def car(env):
    while True:
        print(f"开始停车: {env.now}")
        # 停车的时间为5个时间单位
        parking_duration = 5
        yield env.timeout(parking_duration)

        print(f"开始行驶: {env.now}")
        # 行驶的时间为2个时间单位
        trip_duration = 2
        yield env.timeout(trip_duration)


# 创建一个新的环境
my_env = simpy.Environment()
# 创建新的 process
my_env.process(car(my_env))
# 执行模拟 运行15个时间单位后停止
my_env.run(until=15)
