#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: knn_iris.py 
@time: 2023-07-28
@contact: danerlt001@gmail.com
@desc: 
"""
import time

import numpy as np
import onnx
import onnxruntime as rt
from loguru import logger
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

logger.add("knn_iris.log")

# 导入鸢尾花数据集
iris = datasets.load_iris()

# 获取特征矩阵和目标向量
X = iris.data
y = iris.target

# 划分训练数据和测试数据
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建KNN分类器,并拟合模型
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# 对测试数据进行预测
start = time.perf_counter()
y_pred = knn.predict(X_test)
end = time.perf_counter()
logger.info(f"KNN算法预测耗时: {end - start}秒")
logger.info(f"预测结果：{y_pred}")

# 计算预测准确率
accuracy = np.mean(y_pred == y_test) * 100
logger.info(f"KNN算法预测准确率: {accuracy}")

# 保存模型 保存为onnx格式
initial_type = [('float_input', FloatTensorType([None, 4]))]
onnx_model = convert_sklearn(knn, initial_types=initial_type)
onnx.save(onnx_model, "knn.onnx")

# 加载模型
sess = rt.InferenceSession("knn.onnx")

input_name = sess.get_inputs()[0].name
label_name = sess.get_outputs()[0].name

start = time.perf_counter()
pred_onnx = sess.run([label_name], {input_name: X_test.astype(np.float32)})[0]
end = time.perf_counter()
logger.info(f"ONNX模型预测耗时: {end - start}秒")

# 2023-07-28 17:11:02.651 | INFO     | __main__:<module>:42 - KNN算法预测耗时: 0.002080800000000771秒
# 2023-07-28 17:11:02.652 | INFO     | __main__:<module>:43 - 预测结果：[1 0 2 1 1 0 1 2 1 1 2 0 0 0 0 1 2 1 1 2 0 2 0 2 2 2 2 2 0 0]
# 2023-07-28 17:11:02.652 | INFO     | __main__:<module>:47 - KNN算法预测准确率: 100.0
# 2023-07-28 17:11:02.716 | INFO     | __main__:<module>:63 - ONNX模型预测耗时: 0.001147500000000079秒
