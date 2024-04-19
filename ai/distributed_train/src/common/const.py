#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: const.py
@time: 2023-12-20
@contact: danerlt001@gmail.com
@desc: 
"""
from pathlib import Path

# 时间格式 年-月-日 时:分:秒
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
# 日期格式 年-月-日
DATE_FORMAT = "%Y-%m-%d"
# 默认时区 北京时间  数据库存的时间是 北京时间
DEFAULT_TIMEZONE = 8
DEFAULT_TIMEZONE_STR = "Asia/Shanghai"

# 路径配置相关 const.py
current_path: Path = Path(__file__)
# common目录路径
COMMON_PATH: Path = current_path.parent
# src目录路径
SRC_PATH: Path = COMMON_PATH.parent
# 项目根路径
ROOT_PATH: Path = SRC_PATH.parent
# data目录路径
DATA_PATH: Path = ROOT_PATH.joinpath("data")
# logs目录路径
LOG_PATH: Path = ROOT_PATH.joinpath("logs")
