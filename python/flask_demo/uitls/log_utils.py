#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: log_utils.py
@time: 2022-08-10
@contact: danerlt001@gmail.com
@desc: 日志工具类
"""

import os

import sys
import logging
from logging.handlers import TimedRotatingFileHandler

from common import config


def init_logger(logger_name, filename):
    logger = logging.getLogger(logger_name)

    logger_level = config.LOGGER_CONFIG.get("level", logging.INFO)
    logger.setLevel(logger_level)

    format_str = '%(asctime)s %(levelname)s [%(filename)s.py %(lineno)d %(funcName)s] %(message)s'
    formatter = logging.Formatter(format_str)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # 用于记录到文件的处理程序，以特定的时间间隔轮换日志文件。如果 backupCount > 0，则在完成翻转后，
    # 将保留不超过 backupCount 个文件, 最旧的文件将被删除。
    # 日志轮转的单位 默认为D 表示天  S：秒 M：分钟 H：小时 D：天
    when = config.LOGGER_CONFIG.get("when", "D")
    # 日志轮转的间隔 默认7天
    interval = config.LOGGER_CONFIG.get("interval", 7)
    # 已经轮转的日志文件最大保留个数 默认30天
    backup_cunt = config.LOGGER_CONFIG.get("backup_count", 30)
    file_handler = TimedRotatingFileHandler(filename, when=when, interval=interval, backupCount=backup_cunt,
                                            encoding='utf-8')
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def init_loggers():
    """初始化日志
    :param
    """
    try:
        import tensorflow as tf
        tf.logging.set_verbosity(tf.logging.ERROR)
    except Exception:
        pass
    # workspace is current dir
    current_path = os.path.abspath(__file__)
    utils_path = os.path.dirname(current_path)
    root_path = os.path.dirname(utils_path)  # 项目目录
    logger_dir_name = config.LOGGER_CONFIG.get("file_path", "app_logs")
    logdir = os.path.join(root_path, logger_dir_name)  # 项目日志目录
    if not os.path.exists(logdir):
        os.mkdir(logdir)

    logger_dict = {
        "api": "api.log",
        "job": "job.log",
        "run": "run.log",
        "warning": "warning.log"
    }
    for logger_name, log_file in logger_dict.items():
        init_logger(logger_name, os.path.join(logdir, log_file))


init_loggers()
