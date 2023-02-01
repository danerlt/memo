#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
"""
@desc: 冒泡排序
"""
import random
from typing import List


def sort(arr: List) -> List:
    """冒泡排序(升序)

    它会遍历若干次要排序的数列，每次遍历时，它都会从前往后依次的比较相邻两个数的大小；
    如果前者比后者大，则交换它们的位置。
    这样，一次遍历之后，最大的元素就在数列的末尾！
    采用相同的方法再次遍历时，第二大的元素就被排列在最大元素之前。
    重复此操作，直到整个数列都有序为止！
    :param arr: 
    :return: 
    """
    length = len(arr)
    for i in range(length - 1, 0, -1):
        for j in range(0, i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def t_sort():
    array = [random.randint(0, 100) for i in range(10)]
    print(array)
    sort_array = sort(array)
    print(sort_array)


if __name__ == '__main__':
    t_sort()
