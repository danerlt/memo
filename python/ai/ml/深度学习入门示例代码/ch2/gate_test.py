#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: gete_test.py
@time: 2024-01-03
@contact: danerlt001@gmail.com
@desc: 感知机测试
"""
import numpy as np


def and_gate(x1, x2):
    """与门（AND gate）

    与门是有两个输入和一个输出的门电路，与门仅在两个输入均为1时输出1，其他时候则输出0。

    真值表如下：
    +----+----+---+
    | x1 | x2 | y |
    +====+====+===+
    | 0  | 0  | 0 |
    | 0  | 1  | 0 |
    | 1  | 0  | 0 |
    | 1  | 1  | 1 |
    +----+----+---+

    Args:
        x1: 输入1
        x2: 输入2

    Returns: 真值：1 或者 0

    """
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.7
    tmp = np.sum(w * x) + b
    if tmp <= 0:
        return 0
    else:
        return 1


def nand_gate(x1, x2):
    """与非门（NAND gate）

    NAND是Not AAND的意思，与非门颠倒了与门的输出。

    真值表如下：
    +----+----+---+
    | x1 | x2 | y |
    +====+====+===+
    | 0  | 0  | 1 |
    | 0  | 1  | 1 |
    | 1  | 0  | 1 |
    | 1  | 1  | 0 |
    +----+----+---+

    Args:
        x1: 输入1
        x2: 输入2

    Returns: 真值：1 或者 0

    """
    x = np.array([x1, x2])
    w = np.array([-0.5, -0.5])
    b = 0.7
    tmp = np.sum(w * x) + b
    if tmp <= 0:
        return 0
    else:
        return 1


def or_gate(x1, x2):
    """或门

    或门是有两个输入和一个输出的门电路，或门只要有一个输入为1时输出1，其他时候则输出0。

    真值表如下：
    +----+----+---+
    | x1 | x2 | y |
    +====+====+===+
    | 0  | 0  | 0 |
    | 0  | 1  | 1 |
    | 1  | 0  | 1 |
    | 1  | 1  | 1 |
    +----+----+---+

    Args:
        x1: 输入1
        x2: 输入2

    Returns: 真值：1 或者 0

    """
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.2
    tmp = np.sum(w * x) + b
    if tmp <= 0:
        return 0
    else:
        return 1


def xor_gate(x1, x2):
    """异或门

    当x1或x2中的一方为1时，才会输出1（“异或”是拒绝其他的意思）

    下面这个是通过真值表归纳出来的
    x1 xor x2 = (x1 or x2) and (x1 nand x2)
    真值表如下：
    +----+----+---+
    | x1 | x2 | y |
    +====+====+===+
    | 0  | 0  | 0 |
    | 0  | 1  | 1 |
    | 1  | 0  | 1 |
    | 1  | 1  | 0 |
    +----+----+---+

    Args:
        x1: 输入1
        x2: 输入2

    Returns:真值：1 或者 0

    """
    s1 = or_gate(x1, x2)
    s2 = nand_gate(x1, x2)
    y = and_gate(s1, s2)
    return y


def test_gate():
    x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    for item in x:
        x1 = item[0]
        x2 = item[1]
        and_y = and_gate(x1, x2)
        nand_y = nand_gate(x1, x2)
        or_y = or_gate(x1, x2)
        xor_y = xor_gate(x1, x2)
        print(f"|{x1=}, {x2=} | x1 and x2 = {and_y} | x1 nand x2 = {nand_y} | x1 or x2 = {or_y} | x1 xor x2 = {xor_y}")


def main():
    test_gate()


if __name__ == '__main__':
    main()
