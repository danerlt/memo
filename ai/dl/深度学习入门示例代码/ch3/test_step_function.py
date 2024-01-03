#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: test_step_function.py
@time: 2024-01-03
@contact: danerlt001@gmail.com
@desc: 
"""
import numpy as np
import matplotlib.pylab as plt


def setp_function(x):
    """
    阶跃函数
    :param x:
    :return:
    """
    return np.array(x > 0, dtype=int)


def show_step_function():
    x = np.arange(-5.0, 5.0, 0.1)  # 生成x，范围为-5到5，步长为0.1
    y = setp_function(x)
    plt.plot(x, y)
    plt.ylim(-0.1, 1.1)  # 设置y轴范围
    plt.show()


def main():
    show_step_function()


if __name__ == '__main__':
    main()
