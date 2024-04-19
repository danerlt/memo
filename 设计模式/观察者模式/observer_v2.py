#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
from abc import ABCMeta, abstractmethod

"""
Observer 是观察者的抽象类。
addObserver、removeObserver分别用于添加和删除观察者，
notifyObservers 用于内容或状态变化时通知所有的观察者。

Observable 是被观察者的抽象类.

因为Observable 的 notifyObservers 会调用 Observer 的 update 方法，所有观察者不需要关心被观察的对象什么时候会发生变化，
只要有变化就会自动调用 update，所以只需要关注 update 实现就可以了。


在设计监听模式的程序时要注意以下几点。
（1）要明确谁是观察者谁是被观察者，只要明白谁是应该关注的对象，问题也就明白了。
一般观察者与被观察者之间是多对一的关系，一个被观察对象可以有多个监听对象（观察者）。
如一个编辑框，有鼠标点击的监听者，也有键盘的监听者，还有内容改变的监听者。
（2）Observable 在发送广播通知的时候，无须指定具体的 Observer，Observer 可以自己决
定是否订阅 Subject 的通知。
（3）被观察者至少需要有三个方法：添加监听者、移除监听者、通知 Observer 的方法。观
察者至少要有一个方法：更新方法，即更新当前的内容，做出相应的处理。
（4）添加监听者和移除监听者在不同的模型称谓中可能会有不同命名，如在观察者模型中
一般是 addObserver/removeObserver；在源/监听器（Source/Listener）模型中一般是 attach/detach，
应用在桌面编程的窗口中还可能是 attachWindow/detachWindow 或 Register/UnRegister。不要被
名称弄迷糊了，不管它们是什么名称，其实功能都是一样的，就是添加或删除观察者。
"""


# 引入 ABCMeta 和 abstractmethod 来定义抽象类和抽象方法
class Observer(metaclass=ABCMeta):
    """观察者的基类"""

    @abstractmethod
    def update(self, observable, observer=None):
        raise NotImplementedError()


class Observable:
    """被观察者的基类"""

    def __init__(self):
        self.__observers = []

    def add_observer(self, observer: Observer):
        """添加观察者"""
        self.__observers.append(observer)

    def remove_observer(self, observer: Observer):
        """移除观察者"""
        self.__observers.remove(observer)

    def notify_observers(self, obj=None):
        """通知观察者"""
        for o in self.__observers:
            o.update(self, obj)


class WatherHeater(Observable):
    """热水器

    被观察的对象
    """

    def __init__(self):
        super().__init__()
        self._temprature = 25

    @property
    def temprature(self):
        return self._temprature

    @temprature.setter
    def temprature(self, value):
        self._temprature = value
        print(f"当前温度是{self._temprature}℃")
        self.notify_observers()


class WashingMode(Observer):
    """洗澡模式"""

    min_temprature = 37
    max_temprature = 50

    def update(self, observalable: Observable, obj=None):
        if isinstance(observalable, WatherHeater) and (
                self.min_temprature <= observalable.temprature < self.max_temprature):
            print(f"水已烧好,可以用来洗澡了.")


class DrinkMode(Observer):
    """饮水模式"""
    drink_tmperature = 100

    def update(self, observalable: Observable, obj=None):
        if isinstance(observalable, WatherHeater) and observalable.temprature >= self.drink_tmperature:
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
