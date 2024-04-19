#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@file: main.py
@time: 2023-02-14
@desc:非线性反向传播

x    |   a      |     b      |     c        |  y
x=2  |  a=x*x   |   b=ln(a)  |   c=sqrt(b)  |


其中 1<x<=10, 0<y<2.15
假设有5个人代码x,a,b,c,y
提出问题：假设我们想最后得到 c=2.13的值，x应该是多少？（误差小于10e-6即可）

参考链接
https://microsoft.github.io/ai-edu/%E5%9F%BA%E7%A1%80%E6%95%99%E7%A8%8B/A2-%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C%E5%9F%BA%E6%9C%AC%E5%8E%9F%E7%90%86/%E7%AC%AC1%E6%AD%A5%20-%20%E5%9F%BA%E6%9C%AC%E7%9F%A5%E8%AF%86/02.2-%E9%9D%9E%E7%BA%BF%E6%80%A7%E5%8F%8D%E5%90%91%E4%BC%A0%E6%92%AD.html



正向过程
1.第1个人,输入层,随即输入一个x的值,假设第一个是2
2.第2个人,第一层网络计算,接收第1个人传入的x的值,计算a=x**2
3.第3个人,第二层网络计算,接收第2个人传入的a的值,计算b=ln(a)
4.第4个人,第三层网络计算,接收第3个人传入的b的值,计算c=sqrt(b)
5.第5个人,输出层,接收第4个人传入的c的值


反向过程
1.第5个人,计算y和c的差值: delta_c = c - y, 传回给第4个人
2.第4个人,接收第5个人传回的delta_c:,计算 delta_b = delet_c * 2 * sqrt(b)
3.第3个人,接收第4个人传回的delta_b:,计算 delta_a = delta_b * a
4.第2个人,接收第3个人传回的delta_a:,计算 delta_x = delta_a / (2*x)
5.第1个人,接收第2个人传回的delta_x:,更新 x = x - delta_x


"""
import math


def first_net(x):
    """ 正向第一层网络
    :param x:
    :return:
    """
    y = x ** 2
    return y


def second_net(x):
    """正向第二层网络

    :param x:
    :return:
    """
    y = math.log(x)
    return y


def thrid_net(x):
    """正向第三层网络

    :param x:
    :return:
    """
    y = math.sqrt(x)
    return y


def noliner_back_propagation(x, y):
    a = first_net(x)
    b = second_net(a)
    c = thrid_net(b)

    delet_c = c - y
    print(f"first a={a}, b={b}, c={c}, y={y}, delet_c: {delet_c}")
    while abs(delet_c) > 1e-6:
        delet_b = 2 * math.sqrt(b) * delet_c
        delet_a = a * delet_b
        delet_x = delet_a / (2 * x)
        x = x - delet_x
        a = first_net(x)
        b = second_net(a)
        c = thrid_net(b)
        delet_c = c - y
        print(f"loop a={a}, b={b}, c={c}, y={y}, delet_c: {delet_c}, delet_b: {delet_b}, delet_a: {delet_a}, delet_x: {delet_x}")

    print("done!")
    print(f"x={x}, y={y}, c: {c}")


if __name__ == '__main__':
    init_x = 2
    target = 2.13
    noliner_back_propagation(init_x, target)
