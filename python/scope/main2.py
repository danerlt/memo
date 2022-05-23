#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
a = "hello"


def main():
    global a
    print(f"global a is {a}, address: {id(a)}")
    a = "hello"
    print(f"local a is {a}, address: {id(a)}")
    for i in range(2):
        a = "hello"
        print(f"for a is {a}, address: {id(a)}")
        if i % 2 != 0:
            a = "hello"
            print(f"if a is {a}, address: {id(a)}")


if __name__ == "__main__":
    main()

# 执行结果
# global a is hello, address: 2087656536688
# local a is hello, address: 2087656536688
# for a is hello, address: 2087656536688
# for a is hello, address: 2087656536688
# if a is hello, address: 2087656536688
