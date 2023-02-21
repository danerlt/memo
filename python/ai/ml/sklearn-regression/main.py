#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt
@file: regression.py
@time: 2023-02-20
@contact: danerlt001@geely.com
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


def linear_function(x):
    """线性回归函数
    y = a * x + b
    """
    y = 3 * x + 5
    return y


def exponetial_function(x):
    """指数回归函数
    y = a * (e ** (b * x)) + c
    """
    y = 124 * (math.e ** (0.15 * x)) + 10
    return y


def logarithm_function(x):
    """对数回归函数
    y = a * ln(x) + b
    """
    y = 4.5 * math.log(x) + 30
    return y


def get_data(func):
    x_list = np.linspace(1, 100, 500)
    train_data = np.array([[x, func(x) + random.randint(0, 5)] for x in x_list], dtype=float)
    x2_list = np.linspace(1, 100, 50) + 0.5 * np.random.random(50)
    test_data = np.array([[x, func(x)] for x in x2_list], dtype=float)
    x_train, y_train = train_data[:, :1], train_data[:, 1]
    x_test, y_test = test_data[:, :1], test_data[:, 1]
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
        (ExponentialRegression(), exponetial_function),  # 指数回归
        (LogarithmRegression(), logarithm_function)  # 对数回归
    ]
    for model, func in maps:
        train(model, func)


if __name__ == '__main__':
    main()
