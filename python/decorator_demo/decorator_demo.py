#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: decorator_demo.py 
@time: 2023-07-31
@contact: danerlt001@gmail.com
@desc: 
"""
from functools import wraps

from loguru import logger

logger.add("dec.log")


def foo(func):
    logger.info("start foo")

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("start foo wrapper")
        res = func(*args, **kwargs)
        logger.info("end foo wrapper")
        return res

    logger.info("end foo")
    return wrapper


def bar(func):
    logger.info("start bar")

    def wrapper(*args, **kwargs):
        logger.info("start bar wrapper")
        res = func(*args, **kwargs)
        logger.info("end bar wrapper")
        return res

    logger.info("end bar")
    return wrapper


@foo
@bar
def abc():
    """abc"""
    logger.info("start abc")


# abc()
# abc = foo(bar(abc))
# abc()

def bar(logger):
    logger.info("start bar")

    def inner(func):
        def wrapper(*args, **kwargs):
            logger.info("start bar wrapper")
            res = func(*args, **kwargs)
            logger.info("end bar wrapper")
            return res

        return wrapper

    logger.info("end bar")
    return inner


@bar(logger)
def cde():
    pass
