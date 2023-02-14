#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@file: main.py
@time: 2023-02-14
@desc: 线性反向传播

假设有一个函数 z = x * y
x = 2w + 3b
y = 2b + 1

目标是使z=150, 求解w和b

初始值使w=3,b=4,则x=18,y=9,z=162
"""


def single_varibale_b(w, b, z):
    """使w值固定,变化b的值 在迭代中没有重新计算贡献值

    :param w:
    :param b:
    :param z: 目标值
    :return:
    """
    print("singel variable : b ---------")
    x = 2 * w + 3 * b
    y = 2 * b + 1
    current_z = x * y
    delta_z = current_z - z
    print(f"first w={w}, b={b}, z={current_z}, delta_z={delta_z}")
    while abs(delta_z) > 0.00001:
        # 对b求偏导可得 dz / db = 63
        delta_b = delta_z / 63
        b = b - delta_b
        x = 2 * w + 3 * b
        y = 2 * b + 1
        current_z = x * y
        delta_z = current_z - z
        print(f"loop w={w}, b={b}, z={current_z}, delta_z={delta_z}")
    print("done!")
    print(f"final w={w}, b={b}")


def single_varibale_new_b(w, b, z):
    """使w值固定,变化b的值 在迭代中重新计算贡献值

    :param w:
    :param b:
    :param z: 目标值
    :return:
    """
    print("singel variable new: b ---------")
    x = 2 * w + 3 * b
    y = 2 * b + 1
    current_z = x * y
    delta_z = current_z - z
    print(f"first w={w}, b={b}, z={current_z}, delta_z={delta_z}")
    while abs(delta_z) > 0.00001:
        # 对b求偏导可得 dz / db = (dz / dx) * (dx / db) + (dz / dy) * (dy / db)
        #                      = [d(x * y) / dx] * [d(2w * 3b)/ db] + [d( x * y ) / dy] * [d(2b + 1) / db]
        #                      = y * 3 + x * 2
        factor_b = (y * 3 + x * 2)
        delta_b = delta_z / factor_b
        b = b - delta_b
        x = 2 * w + 3 * b
        y = 2 * b + 1
        current_z = x * y
        delta_z = current_z - z
        print(f"loop w={w}, b={b}, z={current_z}, delta_z={delta_z}, factor_b: {factor_b}, delta_b: {delta_b}")
    print("done!")
    print(f"final w={w}, b={b}")


def double_varibale_w_b(w, b, z):
    """同时改变w,和b,使结果为z 在迭代中没有重新计算贡献值

    :param w:
    :param b:
    :param z: 目标值
    :return:
    """
    print("double_varibale_w_b, w and b ---------")
    x = 2 * w + 3 * b
    y = 2 * b + 1
    current_z = x * y
    delta_z = current_z - z
    print(f"first w={w}, b={b}, z={current_z}, delta_z={delta_z}")
    while abs(delta_z) > 0.00001:
        # 对b求偏导可得 dz / db = 63
        # 对w为编导得 dz / dw = 18
        # 默认w和b对deleta_z的贡献各占50%
        delta_b = delta_z / 2 / 63
        b = b - delta_b
        delta_w = delta_z / 2 / 18
        w = w - delta_w
        x = 2 * w + 3 * b
        y = 2 * b + 1
        current_z = x * y
        delta_z = current_z - z
        print(f"loop w={w}, b={b}, z={current_z}, delta_z={delta_z}")
    print("done!")
    print(f"final w={w}, b={b}")


def doubele_variable_new_w_b(w, b, z):
    """同时改变w,和b,使结果为z 在迭代中没有重新计算贡献值

    :param w:
    :param b:
    :param z: 目标值
    :return:
    """
    print("doubele_variable_new_w_b,  w and b ---------")
    x = 2 * w + 3 * b
    y = 2 * b + 1
    current_z = x * y
    delta_z = current_z - z
    print(f"first w={w}, b={b}, z={current_z}, delta_z={delta_z}")
    while abs(delta_z) > 0.00001:
        # 对b求偏导可得 dz / db = (dz / dx) * (dx / db) + (dz / dy) * (dy / db)
        #                      = [d(x * y) / dx] * [d(2w * 3b)/ db] + [d( x * y ) / dy] * [d(2b + 1) / db]
        #                      = y * 3 + x * 2
        # 对w求偏导可得 dz / dw =(dz / dx) * (dx / dw) + (dz / dy) * (dy / dw)
        #                     = y * 2 + x * 0
        # 默认w和b对deleta_z的贡献各占50%
        factor_b = y * 3 + x * 2
        delta_b = delta_z / 2 / factor_b
        b = b - delta_b
        factor_w = y * 2
        delta_w = delta_z / 2 / factor_w
        w = w - delta_w
        x = 2 * w + 3 * b
        y = 2 * b + 1
        current_z = x * y
        delta_z = current_z - z
        print(f"loop w={w}, b={b}, z={current_z}, delta_z={delta_z}, "
              f"factor_b: {factor_b}, delta_b: {delta_b}, factor_w: {factor_w}, delta_w: {delta_w}")
    print("done!")
    print(f"final w={w}, b={b}")


if __name__ == '__main__':
    init_w, init_b = 2, 2
    target = 150
    single_varibale_b(init_w, init_b, target)
    single_varibale_new_b(init_w, init_b, target)
    double_varibale_w_b(init_w, init_b, target)
    doubele_variable_new_w_b(init_w, init_b, target)
