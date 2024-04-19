#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: gunicorn_conf.py.py 
@time: 2024-03-21
@contact: danerlt001@gmail.com
@desc: 
"""

import multiprocessing


# 获取CPU核数，with这个是读取docker容器中的配置
try:
    with open("/sys/fs/cgroup/cpu/cpu.cfs_quota_us") as f:
        quota = int(f.read())
        if quota > 0:
            cores = quota // 100000
        else:
            cores = multiprocessing.cpu_count()
except Exception as e:
    print(e)
    cores = multiprocessing.cpu_count()

# 设置workers 通常可以设置成CPU核数*2或者4+1
# 具体设置那个比较好可以做压力测试来判断
workers = cores * 2 + 1
print(f"{workers=}")

#
# worker_class = "meinheld.gmeinheld.MeinheldWorker"  # 使用 Meinheld 代替 gevent， 这个性能更好，但是安装需要编译，比较麻烦
worker_class = "gevent"
keeplive = 10
timeout = 60
threads = 32
preload_app = True
reload = True
x_forwarded_for_header = "X_FORWARDED_FOR"
