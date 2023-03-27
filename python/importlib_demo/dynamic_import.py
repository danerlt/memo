#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: dynamic_import.py 
@time: 2023-03-27
@contact: danerlt001@gmail.com
@desc: 
"""


import importlib.util

# spec_from_file_location是importlib.util模块中的一个函数，用于创建一个模块规范对象。
# 这个函数接受两个参数：name表示要创建的模块的名称，location表示模块所在的文件路径。
# location参数是字符串（str）或pathlib.Path对象
# 创建模块规范对象
spec = importlib.util.spec_from_file_location('my_module', './my_module.py')

# 加载模块
my_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(my_module)

# 使用模块中的函数
my_module.my_function()  # 输出：Hello, world!