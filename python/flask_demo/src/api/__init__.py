#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: __init__.py.py 
@time: 2022-10-16
@contact: danerlt001@gmail.com
@desc: 
"""

import importlib
from pathlib import Path
from utils.logutil import creater_logger

logger = creater_logger()

current_path = Path(__file__).parent


def import_api(path, base_path: str):
    """
    动态导入所有api，导入api目录下的py文件
    :param path: Node
    :param base_path: 基本前缀 str类型
    :return:
    """
    logger.info(f"path: {path}, base_path: {base_path}")
    if path is None:
        path = Path(__file__).parent
    files = path.iterdir()
    for file in files:
        if not file.name.startswith("__"):
            # 排除掉 __pycache__ 目录 和__init__.py
            if file.is_dir():
                import_api(file, base_path + "." + file.name)
            elif file.is_file() and file.suffix == ".py":
                importlib.import_module(base_path + '.' + file.stem)


import_api(None, 'api')
