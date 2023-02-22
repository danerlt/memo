#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: customer_regression.py
@time: 2023-02-21
@contact: danerlt001@gmail.com
@desc: 指数回归运算
"""

import math
import random

import matplotlib.pyplot as plt
import numpy as np
from sklearn.base import RegressorMixin
from sklearn.model_selection import train_test_split


class MyLinearRegression(RegressorMixin):
    """线性回归
    
    公式: y = kx +b
    """

    def __init__(self):
        self.k = 1
        self.b = 0
        self.expression = ""

    def fit(self, X, y):
        sumX = np.sum(X)
        sumY = np.sum(y)
        sumXY = np.sum(X * y)
        sumXX = np.sum(X * X)
        length = len(X)
        self.k = ((length * sumXY) - (sumX * sumY)) / ((length * sumXX) - (sumX * sumX))
        self.b = (sumY / length) - ((self.k * sumX) / length)
        self.expression = f"y = {self.k}x+{self.b}"
        print(f"MyLinearRegression expression: {self.expression}")

    def predict(self, X):
        y_predict = []
        for x_i in X:
            y = self.k * x_i + self.b
            y_predict.append(y)
        res = np.array(y_predict, dtype=float)
        return res


class MyExponentialRegression(RegressorMixin):
    """指数回归

    公式: y = a*e^bx
    """

    def __init__(self):
        self.a = 1
        self.b = 1
        self.expression = ""

    def fit(self, X, y):
        sumY = np.sum(y)
        sumXXY = np.sum(X * X * y)
        sumYlny = np.sum(y * np.log(y))
        sumXYlny = np.sum(X * y * np.log(y))
        sumXY = np.sum(X * y)
        denominator = (sumY * sumXXY) - (sumXY * sumXY)
        self.a = math.exp((sumXXY * sumYlny - sumXY * sumXYlny) / denominator)
        self.b = (sumY * sumXYlny - sumXY * sumYlny) / denominator
        self.expression = f'y = {round(self.a * 100) / 100} * e^{round(self.b * 100) / 100}x'
        print(f"MyExponentialRegression expression: {self.expression}")

    def predict(self, X):
        y_predict = []
        for x_i in X:
            y = self.a * math.exp(self.b * x_i)
            y_predict.append(y)
        res = np.array(y_predict, dtype=float)
        return res


class MyLogarithmRegression(RegressorMixin):
    """对数回归
    
    公式: y = a*ln(x)+b
    """

    def __init__(self):
        self.a = 1
        self.b = 0
        self.expression = ""

    def fit(self, X, y):
        sumlnx = np.sum(np.log(X))
        sumYlnx = np.sum(y * np.log(X))
        sumY = np.sum(y)
        sumlnxlnx = np.sum(np.log(X) * np.log(X))
        length = len(X)
        self.a = (length * sumYlnx - sumY * sumlnx) / (length * sumlnxlnx - sumlnx * sumlnx)
        self.b = (sumY - self.a * sumlnx) / length
        self.expression = f'y = {round(self.a * 100) / 100} * ln(x) + {round(self.b * 100) / 100}'
        print(f"MyLogarithmRegression expression: {self.expression}")

    def predict(self, X):
        y_predict = []
        for x_i in X:
            y = self.a * math.log(x_i) + self.b
            y_predict.append(y)
        res = np.array(y_predict, dtype=float)
        return res


def linear_function(x):
    """线性回归函数
    y = a * x + b
    """
    y = 3 * x + 20
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
    x_list = np.linspace(1, 120, 50)
    data = np.array([[x, func(x) + random.randint(0, 5)] for x in x_list], dtype=float)
    train_data, test_data = train_test_split(data, test_size=0.3)
    x_train, y_train = train_data[:, 0], train_data[:, 1]
    x_test, y_test = test_data[:, 0], test_data[:, 1]
    return np.sort(x_train), np.sort(y_train), np.sort(x_test), np.sort(y_test)


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
    plt.xlabel('x', fontdict={'size': 16})
    plt.ylabel('y', fontdict={'size': 16}, rotation=0)
    plt.plot(x_train, y_train, 'yo-', label='train data')
    # plt.plot(x_test, y_test, 'go-', label='true data')
    plt.plot(x_test, y_predict, 'ro-', label='predict data')
    plt.title('score: %f' % score)
    plt.legend()
    plt.show()


def main():
    maps = [
        (MyLinearRegression(), linear_function),  # 线性回归
        (MyExponentialRegression(), exponetial_function),  # 指数回归
        (MyLogarithmRegression(), logarithm_function)  # 对数回归
    ]
    for model, func in maps:
        train(model, func)


if __name__ == '__main__':
    main()
