#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: my_module.py 
@time: 2023-03-27
@contact: danerlt001@gmail.com
@desc: 
"""


def my_function():
    print('Hello, world!')


l = [2, 3, 1, 4, 5]
s = set(l)
print(s)
s.add(10)
print(s)
s.add(0)
print(s)


from collections import OrderedDict