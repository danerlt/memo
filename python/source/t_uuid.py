#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
"""
@file: t_uuid.py 
@time: 2022-10-14
@desc: 
"""
import datetime
import uuid


def interval_uuid_100ns():
    """计算UUID1时间间隔
    """
    start = datetime.datetime(1582, 10, 15)
    end = datetime.datetime(1970, 1, 1)
    diff = end - start
    seconds = diff.total_seconds()
    ns = seconds * 1e9
    ns_100 = int(ns / 100)
    ns_hex = hex(ns_100)
    print(ns_hex)
    interval = 0x01b21dd213814000
    print(interval == ns_100)  # 结果为True


def t_generate_uuid():
    uuid1 = uuid.uuid1()
    print(uuid1)
    uuid3 = uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org')
    print(uuid3)
    uuid4 = uuid.uuid4()
    print(uuid4)
    uuid5 = uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org')
    print(uuid5)
    x = uuid.UUID('{00010203-0405-0607-0809-0a0b0c0d0e0f}')
    print(x)


if __name__ == '__main__':
    interval_uuid_100ns()
    t_generate_uuid()
