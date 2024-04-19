#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: car2.py 
@time: 2023-04-19
@contact: danerlt001@gmail.com
@desc:
电动汽车在旅行后通常要花很多时间给电池充电。他们必须等到电池充电后才能再次开车。
"""
import random

import simpy


class Car(object):
    def __init__(self, car_id=None, env=None):
        self.id = car_id
        self.env = env
        # 每次创建实例时启动运行进程。
        self.action = env.process(self.run())

    def run(self):
        """汽车的启动函数"""
        while True:
            # 汽车需要充电的时间 2-5个时间单位
            charge_duration = random.randint(2, 5)
            yield self.env.process(self.charge(charge_duration))

            # 汽车的驾驶时间 5-20个时间单位
            trip_duration = random.randint(5, 20)
            yield self.env.process(self.driver(trip_duration))

    def driver(self, duration):
        """汽车的驾驶函数

        :param duration: 驾驶时间
        """
        print(f"now: {self.env.now}, 汽车: {self.id} 开始驾驶, 驾驶时间: {duration}")
        yield self.env.timeout(duration)
        print(f"now: {self.env.now}, 汽车: {self.id} 结束驾驶")

    def charge(self, duration):
        """汽车充电函数

        :param duration: 充电时间
        """
        print(f"now: {self.env.now}, 汽车: {self.id} 开始充电, 需要充电时间: {duration}")
        yield self.env.timeout(duration)
        print(f"now: {self.env.now}, 汽车: {self.id} 结束充电")


def main():
    env = simpy.Environment()
    # 创建5个汽车
    for i in range(5):
        Car(car_id=i, env=env)

    # 执行模拟 运行60个时间单位后停止
    env.run(until=60)


if __name__ == '__main__':
    main()
