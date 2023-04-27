#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: mulit_point.py 
@time: 2023-04-27
@contact: danerlt001@gmail.com
@desc: 
"""

import matplotlib.pyplot as plt

# 创建坐标数组
x1 = [1, 2, 3, 4, 5]
y1 = [2, 4, 6, 8, 10]
x2 = [1.5, 2.5, 3.5, 4.5, 5.5]
y2 = [3, 5, 7, 9, 11]

# 绘制两个点的图形
plt.plot(x1, y1, 'ro', label='Group 1')
plt.plot(x2, y2, 'bs', label='Group 2')

# 添加图例
plt.legend(loc='upper left')

# 显示图形
plt.show()