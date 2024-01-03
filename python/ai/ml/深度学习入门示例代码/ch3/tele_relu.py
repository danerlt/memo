#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: tele_relu.py
@time: 2024-01-03
@contact: danerlt001@gmail.com
@desc: 
"""
import numpy as np
import matplotlib.pyplot as plt


def relu(x):
    res = np.maximum(0, x)
    return res


def show_relu():
    x = np.arange(-5.0, 5.0, 0.1)  # 生成x，范围为-5到5，步长为0.1
    y = relu(x)
    plt.plot(x, y)
    plt.ylim(-0.1, 1.1)  # 设置y轴范围
    plt.show()


def main():
    show_relu()


if __name__ == '__main__':
    main()
