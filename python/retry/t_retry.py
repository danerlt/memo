#!/usr/bin/env python  
# -*- coding:utf-8 -*-

from retry import retry


@retry(ZeroDivisionError, tries=3, delay=1, max_delay=5, backoff=2, jitter=(0, 3))
def bar():
    """如果抛了ZeroDivisionError, 重试3次,每次延迟2秒,最大延迟5秒,每次异常,延迟时间乘以2,每次延迟加上0到3中间的随机秒

    如果还是抛错,将异常抛出"""

    res = 2 / 0
    return res


if __name__ == '__main__':
    import logging

    logging.basicConfig()
    bar()
