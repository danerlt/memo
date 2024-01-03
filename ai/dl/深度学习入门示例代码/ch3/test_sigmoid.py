#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: test_sigmoid.py
@time: 2024-01-03
@contact: danerlt001@gmail.com
@desc: 
"""

import numpy as np
import matplotlib.pyplot as plt


def sigmoid(x):
    res = 1 / (1 + np.exp(-x))
    return res


def show_sigmoid_function():
    x = np.arange(-5.0, 5.0, 0.1)  # 生成x，范围为-5到5，步长为0.1
    y = sigmoid(x)
    plt.plot(x, y)
    plt.ylim(-0.1, 1.1)  # 设置y轴范围
    plt.show()


def main():
    show_sigmoid_function()


if __name__ == '__main__':
    main()
