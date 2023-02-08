#!/usr/bin/env python  
# -*- coding:utf-8 -*-
import os

import tensorflow as tf
from tensorflow import keras

print(tf.__version__)
# 使用第一张GPU卡
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

fashion_mnist = keras.datasets.fashion_mnist
# train_images 和 train_labels 数组为 训练集 的图片和对应的类别。
# test_images 和 test_labels 数组为 测试集 的图片和对应的类别。
# 数据集标签和类别对应关系
# 0	T-shirt/top	T恤/短衫
# 1	Trouser	裤子
# 2	Pullover	套衫
# 3	Dress	裙子
# 4	Coat	大衣
# 5	Sandal	凉鞋
# 6	Shirt	衬衫
# 7	Sneaker	运动鞋
# 8	Bag	包
# 9	Ankle boot	短靴
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()


def pre_process_data():
    """数据预处理"""
    # 将值缩放到 0 和 1 之间
    global train_images
    global test_images
    train_images = train_images / 255.0
    test_images = test_images / 255.0


def create_model():
    """创建model，定义网络

    :return: model
    """
    # Sequential 是模型层的线性叠加 通过堆叠许多层，构建出深度神经网络
    # 网络中的第一个 layer，tf.keras.layers.Flatten 将原始的图片由一个 2d-array (28x28 像素) 转换成一个 1d-array (28 * 28 = 784)。
    # 后面连接了两个tf.keras.layers.Dense 层。这两个层称之为全连接层.
    # 第一个全连接层包含 128 个神经元。
    # 第二层是一个由 10 个节点构成的 softmax 层，该层将返回一个和为 1 的包含 10 个概率值的数组。其中，每个节点的数值表示当前图片属于该类别的概率。
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dense(10, activation=tf.nn.softmax)
    ])
    return model


def compile_model(model):
    """编译模型
    
    :param model: 
    :return: 
    """
    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])


def train_model(model):
    """训练模型

    :param model:
    :return:
    """
    model.fit(train_images, train_labels, epochs=100)


def eval_model(model):
    """评估准确率

    :param model:
    :return:
    """
    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print(f"Test loss: {test_loss}, Test accuracy:{test_acc}")
    return test_acc


def save_model(model):
    """保存模型

    :param model:
    :return:
    """
    model_path = "tf_model.pb"
    tf.keras.models.save_model(model, model_path, overwrite=True, include_optimizer=True)


def main():
    pre_process_data()
    model = create_model()
    compile_model(model)
    train_model(model)
    acc = eval_model(model)
    save_model(model)


if __name__ == '__main__':
    main()
