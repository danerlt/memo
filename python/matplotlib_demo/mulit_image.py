#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: mulit_image.py 
@time: 2023-04-27
@contact: danerlt001@gmail.com
@desc: 
"""

import matplotlib.pyplot as plt
import numpy as np

# 创建一个包含两个子图的画布
fig, axs = plt.subplots(1, 2, figsize=(10,5))

# 生成一些示例数据
x = np.arange(0, 10, 0.1)
y1 = np.sin(x)
y2 = np.cos(x)

# 在第一个子图中绘制 sin(x) 函数
axs[0].plot(x, y1)
axs[0].set_title('Sin(x)')

# 在第二个子图中绘制 cos(x) 函数
axs[1].plot(x, y2)
axs[1].set_title('Cos(x)')

# 显示所有子图
plt.show()