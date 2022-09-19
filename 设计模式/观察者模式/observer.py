#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
from abc import ABCMeta, abstractmethod

"""
刚刚大学毕业的 Tony 只身来到北京这个大城市，开始了北漂生活。但刚刚毕业的
他身无绝技、包无分文，为了生活只能住在沙河镇一个偏僻的村子里，每天坐着程序员
专线（13 号线）穿梭于昌平区与西城区……
在寒冷的冬天，Tony 坐 2 个小时的“地铁+公交”回到住处，拖着疲惫的身体，准
备洗一个热水澡暖暖身体，奈何简陋的房子中用的还是 20 世纪 90 年代的热水器。因为
热水器没有警报，更没有自动切换模式的功能，所以烧热水必须得守着，不然时间长了
成“杀猪烫”，时间短了又“冷成狗”。无奈的 Tony 背靠着墙，头望着天花板，深夜
中做起了白日梦：一定要努力工作，过两个月我就可以自己买一个智能热水器了，水烧
好了就发一个警报，我就可以直接去洗澡。还要能自己设定模式，既可以烧开了用来喝，
又可以烧暖了用来洗澡……




"""


class WatherHeater:
    """热水器"""

    def __init__(self):
        self._observers = []
        # 观察的对象
        self.__temprature = 25  # 室温 

    @property
    def temprature(self):
        return self.__temprature

    @temprature.setter
    def temprature(self, value):
        self.__temprature = value
        print(f"当前温度是{self.__temprature}℃")
        self.notifies()

    def add_observer(self, observer):
        self._observers.append(observer)

    def notifies(self):
        for o in self._observers:
            o.update(self)


class Observer(metaclass=ABCMeta):
    """模式的父类"""

    @abstractmethod
    def update(self, wh: WatherHeater):
        """模式的行为"""
        raise NotImplementedError()


class WashingMode(Observer):
    """洗澡模式"""

    min_temprature = 37
    max_temprature = 50

    def update(self, wh: WatherHeater):
        if self.min_temprature <= wh.temprature < self.max_temprature:
            print(f"水已烧好,可以用来洗澡了.")


class DrinkMode(Observer):
    """饮水模式"""
    drink_tmperature = 100

    def update(self, wh: WatherHeater):
        if wh.temprature >= self.drink_tmperature:
            print(f"水已烧好,可以用来饮用了.")


def t_observer():
    water_heater = WatherHeater()
    wash_mode = WashingMode()
    drink_mode = DrinkMode()
    water_heater.add_observer(wash_mode)
    water_heater.add_observer(drink_mode)

    # 模拟热水器温度升高
    for i in range(0, 101, 20):
        water_heater.temprature = i


if __name__ == '__main__':
    t_observer()
