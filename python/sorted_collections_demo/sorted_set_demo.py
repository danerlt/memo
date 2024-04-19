#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: sorted_set_demo.py 
@time: 2023-03-29
@contact: danerlt001@gmail.com
@desc: SortedSet用法
"""

from sortedcollections import SortedSet


class Element(object):
    def __init__(self, name=None, age=None, sex=None):
        self.name = name
        self.age = age
        self.sex = sex

    def __lt__(self, other):
        return self.age < other.age

    def __gt__(self, other):
        return self.age > other.age

    def __repr__(self):
        return f"Element:<name: {self.name}, age: {self.age}, sex: {self.sex}>"


my_list: list = [Element('a', 2, '男'), Element('b', 3, '女'), Element('c', 1, '男'), Element('d', 4, '女'),
                 Element('e', 5, '男')]

my_ele = Element('f', 0, '男')
my_ele2 = Element('f', 6, '男')

print(my_list)
ss = SortedSet(my_list)
print(ss)
ss.add(my_ele)
print(ss)
ss.add(my_ele2)
print(ss)


se = SortedSet(my_list, key=lambda ele: ele.age)
print(se)
se.add(my_ele)
print(se)
se.add(my_ele2)
print(se)

