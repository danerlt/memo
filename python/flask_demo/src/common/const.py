#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt
@file: const.py 
@time: 2022-08-12
@contact: danerlt001@gmail.com
@desc:  常量定义
"""

# 时间正则表达式 格式： 年-月-日 时:分:秒
import os

RE_TIME = "^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$"
# 时间格式 年-月-日 时:分:秒
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
# 日期格式 年-月-日
DATE_FORMAT = "%Y-%m-%d"
# 默认时区 北京时间  数据库存的时间是 北京时间
DEFAULT_TIMEZONE = 8
DEFAULT_TIMEZONE_STR = "Asia/Shanghai"

# 路径配置相关
current_path = os.path.abspath(__file__)
# common目录路径
COMMON_PATH = os.path.dirname(current_path)
# 项目根路径
ROOT_PATH = os.path.dirname(COMMON_PATH)
# config目录路径
CONFIG_PATH = os.path.join(ROOT_PATH, "config")
# data目录路径
DATA_PATH = os.path.join(ROOT_PATH, "data")
