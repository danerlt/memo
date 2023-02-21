# !/usr/bin/env python
# -*- coding:utf-8 -*-
""" 
@author: danerlt 
@file: demo.py
@time: 2023-02-16
@contact: danerlt001@gmail.com
@desc: scikit-learn常见回归算法
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn import ensemble
from sklearn import linear_model
from sklearn import neighbors
from sklearn import svm
from sklearn import tree


def f(x1, x2):
    """数据生成部分"""
    y = 0.5 * np.sin(x1) + 0.5 * np.cos(x2) + 3 + 0.1 * x1
    return y


def load_data():
    x1_train = np.linspace(0, 50, 500)
    x2_train = np.linspace(-10, 10, 500)
    data_train = np.array([[x1, x2, f(x1, x2) + (np.random.random(1) - 0.5)] for x1, x2 in zip(x1_train, x2_train)])
    x1_test = np.linspace(0, 50, 100) + 0.5 * np.random.random(100)
    x2_test = np.linspace(-10, 10, 100) + 0.02 * np.random.random(100)
    data_test = np.array([[x1, x2, f(x1, x2)] for x1, x2 in zip(x1_test, x2_test)])
    return data_train, data_test


train, test = load_data()
x_train, y_train = train[:, :2], train[:, 2]  # 数据前两列是x1,x2 第三列是y,这里的y有随机噪声
x_test, y_test = test[:, :2], test[:, 2]  # 同上,不过这里的y没有噪声


def try_different_method(model):
    """回归部分"""
    model.fit(x_train, y_train)
    score = model.score(x_test, y_test)
    result = model.predict(x_test)
    plt.figure(figsize=(10, 10))
    plt.plot(np.arange(len(result)), y_test, 'go-', label='true value')
    plt.plot(np.arange(len(result)), result, 'ro-', label='predict value')
    plt.title('score: %f' % score)
    plt.legend()
    plt.show()


def main():
    models = [
        linear_model.LinearRegression(),  # 线性回归
        tree.DecisionTreeRegressor(),  # 决策树回归
        svm.SVR(),  # SVM回归
        neighbors.KNeighborsRegressor(),  # K邻近树回归
        ensemble.RandomForestRegressor(n_estimators=20),  # 随机森林回归 这里使用20个决策树
        ensemble.AdaBoostRegressor(n_estimators=50),  # Adaboost回归 这里使用50个决策树
        ensemble.GradientBoostingRegressor(n_estimators=100),  # GBRT回归 这里使用100个决策树
        ensemble.BaggingRegressor(),  # Bagging回归
        tree.ExtraTreeRegressor(),  # ExtraTree极端随机树回归
    ]
    for model in models:
        try_different_method(model)


if __name__ == '__main__':
    main()
