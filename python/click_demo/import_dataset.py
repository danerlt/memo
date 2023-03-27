#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: import_dataset.py 
@time: 2023-03-27
@contact: danerlt001@gmail.com
@desc: 
"""
import logging
import os
from pathlib import Path

import click

logger = logging.getLogger()


@click.command()
@click.option("-e", "--env", default="dev", show_default=True, help="环境名称")
@click.option("-t", "--dataset_type", default="文本", show_default=True, help="数据集类型")
@click.option("-f", "--is_update_file", is_flag=True, show_default=True, default=True,
              help="上传数据集的时候是否上传文件")
def import_dataset(env, dataset_type, is_update_file):
    """导入数据集"""
    logger.info(f"开始导入数据集, 环境: {env}, 数据集类型: {dataset_type}, 是否上传文件: {is_update_file}")
    pass


def main():
    import_dataset()


if __name__ == '__main__':
    main()
