#!/usr/bin/env python  
# -*- coding:utf-8 -*-
import datetime

from tenacity import retry, wait_fixed, stop_after_attempt, stop_after_delay, retry_if_exception_type, wait_random, \
    wait_exponential


def get_now():
    fmt = "%Y-%m-%d %H:%M:%S"
    now = datetime.datetime.now().strftime(fmt)
    return now


def foo():
    now = get_now()
    print(f"等待重试...: now: {now}")
    a = 1
    b = 0
    print(f"a: {a}, b:{b}")
    res = a / b
    return res


@retry
def t_retry():
    foo()


@retry(wait=wait_fixed(2))
def t_retry_awit():
    """等待两秒,一直重试,直到运行成功"""
    foo()


@retry(wait=wait_random(min=1, max=2))
def t_retry_wait_random_1_to_2_s():
    """一直重试,每次重试等待1到2秒"""
    foo()


@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
def t_retry_wait_exponential_1():
    """一直重试,每次重试等待2 ^ x * multiplier 秒, 最小4秒,最大10秒, 指数默认为2
    关键词: 指数退避
    """
    foo()


@retry(wait=wait_fixed(3) + wait_random(0, 2))
def t_retry_wait_fixed_jitter():
    """等待 3秒+0到2秒随机延迟"""
    foo()


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def t_retry_wait_count():
    """等待重试3次,每次重试等待2秒"""
    foo()


@retry(stop=stop_after_delay(10), wait=wait_fixed(2))
def t_retry_wait_time():
    """重试10秒后不在重试, 每次重试等待2秒"""
    foo()


@retry(stop=(stop_after_delay(10) | stop_after_attempt(7)), wait=wait_fixed(2))
def t_retry_wait_time_or_count():
    """重试10秒后或者重试7次不在重试, 每次重试等待2秒"""
    foo()


@retry(retry=retry_if_exception_type(ZeroDivisionError), wait=wait_fixed(2))
def t_retry_in_exception():
    """如果抛了ZeroDivisoinError就重试,每次重试等待2秒"""
    foo()


@retry(retry=retry_if_exception_type(ZeroDivisionError), stop=stop_after_attempt(3), wait=wait_fixed(2), reraise=True)
def t_retry_raise_origin_exception():
    """如果抛了ZeroDivisoinError就重试,重试3次,每次重试等待2秒,如果最终还是失败抛出原来的异常"""
    foo()


def error_callback(retry_state):
    """retry失败的回调函数,必须要传retry_state参数"""
    print("失败执行回调函数")
    exception = retry_state.outcome.exception
    print(f"exception: {exception}")


@retry(retry_error_callback=error_callback, stop=stop_after_attempt(3), wait=wait_fixed(2), reraise=True)
def t_retry_error_callback():
    """重试最终失败调用回调函数,重试3次,每次重试等待2秒,如果最终还是失败抛出原来的异常"""
    foo()


if __name__ == '__main__':
    # t_retry()
    # t_retry_awit()
    # t_retry_wait_random_1_to_2_s()
    # t_retry_wait_exponential_1()
    # t_retry_wait_fixed_jitter()
    # t_retry_wait_count()
    # t_retry_wait_time()
    # t_retry_wait_time_or_count()
    # t_retry_in_exception()
    # t_retry_raise_origin_exception()
    t_retry_error_callback()
