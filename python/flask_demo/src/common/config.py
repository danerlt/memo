#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: config.py 
@time: 2022-08-10
@contact: danerlt001@gmail.com
@desc: 读取配置文件，初始化项目相关配置
"""

import yaml
import logging

from common.const import COMMON_CONFIG_PATH, MODEL_CONFIG_PATH

logger = logging.getLogger("run")


def get_config(path, name=None):
    logger.debug(f"get_config path: {path}, name: {name}")
    with open(path, "r", encoding="utf-8") as f:
        yaml_dict = yaml.load(f, Loader=yaml.FullLoader)
        if name:
            cfg = yaml_dict.get(name)
            if cfg is None:
                raise Exception(f"获取{name}配置失败，配置不存在")
            logger.debug(f"get_config path: {path}, name: {name}, result: {cfg}")
            return cfg
        else:
            logger.debug(f"get_config path: {path}, result: {yaml_dict}")
            return yaml_dict


# 日志配置
LOGGER_CONFIG = get_config(COMMON_CONFIG_PATH, "logger")
# 任务配置
JOB_CONFIG = get_config(COMMON_CONFIG_PATH, "job")
# 告警配置
WARNING_CONFIG = get_config(COMMON_CONFIG_PATH, "warning")
# MySQL配置
MYSQL_CONFIG = get_config(COMMON_CONFIG_PATH, "mysql")


# 训练相关配置
TRAIN_CONFIG = get_config(MODEL_CONFIG_PATH, "train")
