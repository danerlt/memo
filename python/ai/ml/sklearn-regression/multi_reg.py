#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt
@file: regression.py
@time: 2023-02-20
@contact: danerlt001@gmail.com
@desc: 回归算法样例

"""

import math
import random

import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.linear_model import LinearRegression


class ExponentialRegression(LinearRegression):
    """指数回归"""

    def fit(self, X, y, sample_weight=None):
        ln_y = np.log(y)
        res = super().fit(X, ln_y, sample_weight=sample_weight)
        return res

    def predict(self, X):
        ln_y = super().predict(X)
        y = np.exp(ln_y)
        return y


class LogarithmRegression(LinearRegression):
    """对数回归"""

    def fit(self, X, y, sample_weight=None):
        x_trans = np.log(X)
        res = super().fit(x_trans, y, sample_weight=sample_weight)
        return res

    def predict(self, X):
        x_trans = np.log(X)
        y = super().predict(x_trans)
        return y


def linear_function(x1, x2, x3, x4):
    """线性回归函数
    y = a * x + b
    """
    y = 3 * x1 + 2 * x2 + 4 * x3 + 5 * x4 + 100
    return y


def exponetial_function(x):
    """指数回归函数
    y = a * (e ** (b * x))
    """
    y = 124 * (math.e ** (0.15 * x))
    return y


def logarithm_function(x):
    """对数回归函数
    y = a * ln(x) + b
    """
    y = 4.5 * math.log(x) + 300
    return y


def get_data(func):
    x1_list = np.linspace(1, 100, 500)
    x2_list = np.linspace(1, 100, 500) + 0.1 * np.random.random(500)
    x3_list = np.linspace(1, 100, 500) + 0.2 * np.random.random(500)
    x4_list = np.linspace(1, 100, 500) + 0.3 * np.random.random(500)

    length = len(x1_list)
    train_data = []
    for i in range(length):
        x1 = x1_list[i]
        x2 = x2_list[i]
        x3 = x3_list[i]
        x4 = x4_list[i]
        y = func(x1, x2, x3, x4) + random.randint(0, 10)
        row = [x1, x2, x3, x4, y]
        train_data.append(row)

    train_data = np.array(train_data, dtype=float)

    x1_list = np.linspace(100, 200, 50) + 0.4 * np.random.random(50)
    x2_list = np.linspace(100, 200, 50) + 0.7 * np.random.random(50)
    x3_list = np.linspace(100, 200, 50) + 0.8 * np.random.random(50)
    x4_list = np.linspace(100, 200, 50) + 0.9 * np.random.random(50)
    length = len(x1_list)
    test_data = []
    for i in range(length):
        x1 = x1_list[i]
        x2 = x2_list[i]
        x3 = x3_list[i]
        x4 = x4_list[i]
        y = func(x1, x2, x3, x4)
        row = [x1, x2, x3, x4, y]
        test_data.append(row)

    test_data = np.array(test_data, dtype=float)

    x_train, y_train = train_data[:, :4], train_data[:, 4]
    x_test, y_test = test_data[:, :4], test_data[:, 4]
    return x_train, y_train, x_test, y_test


def train(model, func):
    # 数据预处理
    # 训练模型
    # 验证模型
    # 保存模型
    # 预测模型
    x_train, y_train, x_test, y_test = get_data(func)
    model.fit(x_train, y_train)
    score = model.score(x_test, y_test)
    print(f"score: {score}")
    y_predict = model.predict(x_test)
    # diff = y_test - y_predict

    # 画图
    plt.figure(figsize=(10, 10))
    plt.plot(np.arange(len(y_test)), y_test, 'go-', label='true data')
    plt.plot(np.arange(len(y_predict)), y_predict, 'ro-', label='predict data')
    plt.title('score: %f' % score)
    plt.legend()
    plt.show()


def main():
    maps = [
        (linear_model.LinearRegression(), linear_function),  # 线性回归
        # (ExponentialRegression(), exponetial_function),  # 指数回归
        # (LogarithmRegression(), logarithm_function)  # 对数回归
    ]
    for model, func in maps:
        train(model, func)


if __name__ == '__main__':
    main()
