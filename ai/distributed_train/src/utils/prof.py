#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: prof.py
@time: 2023-12-21
@contact: danerlt001@gmail.com
@desc: 
"""
from functools import wraps
from torch.cuda import memory_allocated, device_count


def get_all_gpu_memory_msg(device_id=None):
    msgs = []
    device_ids = []
    if device_id is None:
        device_ids = list(range(device_count()))
    else:
        device_ids.append(device_id)
    for i in device_ids:
        mem = memory_allocated(i) / 1024 / 1024
        msg = f"GPU {i} memory usage: {mem} MB"
        msgs.append(msg)
    res = ", ".join(msgs)
    return res


def show_all_gpu_memory(logger=None, note="", device_id=None):
    gpu_mem = get_all_gpu_memory_msg(device_id=device_id)
    if logger is None:
        print(f"{note}, {gpu_mem}")
    else:
        logger.info(f"{note}, {gpu_mem}")


def profile(logger=None):
    def wrap(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                logger.info(f"before execute {func.__name__}, {get_all_gpu_memory_msg()}")
                result = func(*args, **kwargs)
                logger.info(f"after execute {func.__name__}, {get_all_gpu_memory_msg()}")
            except Exception:
                raise
            else:
                return result

        return wrapper

    return wrap
