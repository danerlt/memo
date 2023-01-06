#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: 1.py 
@time: 2022-10-18
@contact: danerlt001@gmail.com
@desc: 
"""
import string


def map_func(s):
    """
    k -> m
    o -> q
    e -> g
    :param s:
    :return:
    """

    chars_map = {chr(ord("a") + i): chr(ord("a") + ((i + 2) % 26)) for i in range(26)}
    print(chars_map)
    res = ""
    for char in s:
        origin_char = chars_map.get(char, char)
        res += origin_char
    return res


if __name__ == '__main__':
    s = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
    result = map_func(s)
    print(result)
    s2 = "everybody thinks twice before solving this."
    result = map_func(s2)
    print(result)

