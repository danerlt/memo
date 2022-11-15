#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt
@file: function_pass_variable.py 
@time: 2022-11-15
@contact: danerlt001@gmail.com
@desc: Python 函数参数传递
"""
from typing import Any
from typing import Hashable


def foo(param: Any):
    print(f"start in function : {foo.__name__}, param addr is: {id(param)}, param type is {type(param)}, param value is {param}")
    if isinstance(param, int):
        param += 1
    elif isinstance(param, float):
        param *= 2.5
    elif isinstance(param, str):
        param += "test"
    elif isinstance(param, list):
        param.append(1)
    elif isinstance(param, tuple):
        param = tuple([1, 2, 3])
    elif isinstance(param, set):
        param.add(2)
    elif isinstance(param, dict):
        param["hello"] = "world"
    else:
        pass
    print(f"end of function : {foo.__name__}, param addr is: {id(param)}, param type is {type(param)}, param value is {param}")


def t_foo(param):
    print(f"before call function : {foo.__name__}, param addr is: {id(param)}, param type is {type(param)}, param value is {param}")
    foo(param)
    print(f"after call function : {foo.__name__}, param addr is: {id(param)}, param type is {type(param)}, param value is {param}\n\n")


def main():
    a = 1
    t_foo(a)
    b = 1.1
    t_foo(b)
    c = "hello "
    t_foo(c)
    d = [1, 2, 3]
    t_foo(d)
    e = (1, 2, 3, 4)
    t_foo(e)
    f = set([1])
    t_foo(f)
    g = {"name": "test"}
    t_foo(g)


if __name__ == '__main__':
    main()
