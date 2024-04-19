#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: process.py 
@time: 2022-09-07
@contact: danerlt001@gmail.com
@desc: 多进程处理工具类
"""
import logging
from multiprocessing import Process, Queue

logger = logging.getLogger("run")


def job_process(function, *args, **kwargs):
    """任务进程

    :param function: 任务对应的函数
    :param args: 任务的位置参数
    :param kwargs:  任务的关键字参数
    :return:
    """
    logger.debug(f"start job_process, function: {function.__name__}, args: {args}, kwargs: {kwargs}")
    queue = Queue()
    process = Process(target=run_job_process, args=(function, queue,),
                      kwargs={"func_args": args, "func_kwargs": kwargs})
    process.start()
    result = queue.get()
    process.join()
    process.kill()
    logger.debug(f"end job_process, function: {function.__name__}, result: {result}")
    return result


def run_job_process(func, queue, func_args=None, func_kwargs=None):
    """进程实际执行的函数

    :param func: 任务对应的函数
    :param queue: 队列
    :param func_args: 函数关键字参数
    :param func_kwargs: 参数位置参数
    :return:
    """
    logger.debug(f"start run_job_process, function: {func.__name__}, func_args: {func_args}, kwargs: {func_kwargs}")
    try:
        result = func(*func_args, **func_kwargs)
    except Exception as e:
        logger.exception(e)
        result = e
    logger.debug(f"end run_job_process, result: {result}")
    queue.put(result)
