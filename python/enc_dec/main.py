#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@file: main.py.py
@time: 2023-02-15
@desc:
"""

from cryptography.fernet import Fernet


class EncTools(object):
    def __init__(self):
        self.key = Fernet.generate_key()
        self.f = Fernet(self.key)

    def enc(self, origin: bytes):
        res = self.f.encrypt(origin)
        return res

    def dec(self, enc_str: bytes):
        res = self.f.decrypt(enc_str)
        return res


enc_toos = EncTools()

if __name__ == '__main__':
    s = b"hello world"
    print(f"origin: {s}")
    des_str = enc_toos.enc(s)
    print(f"des_str: {des_str}")
    enc_res = enc_toos.dec(des_str)
    print(f"enc_res: {enc_res}")

    with open("a.txt", "rb") as f:
        a_bytes = f.read()
        enc_a = enc_toos.enc(a_bytes)
        with open("a1.txt", "wb") as f2:
            f2.write(enc_a)

        with open("a1.txt", "rb") as f3:
            enc_a_bytes = f3.read()
            dec_a_byes = enc_toos.dec(enc_a_bytes)
            print(a_bytes == dec_a_byes)
