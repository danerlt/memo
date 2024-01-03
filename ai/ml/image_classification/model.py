#!/usr/bin/env python  
# -*- coding:utf-8 -*-
import os
import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator

base_dir = 'cats_and_dogs_filtered'

train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')

# 猫/狗训练图片目录
train_cats_dir = os.path.join(train_dir, 'cats')
train_dogs_dir = os.path.join(train_dir, 'dogs')

# 猫/狗测试图片目录
validation_cats_dir = os.path.join(validation_dir, 'cats')
validation_dogs_dir = os.path.join(validation_dir, 'dogs')

train_cat_fnames = os.listdir(train_cats_dir)
train_dog_fnames = os.listdir(train_dogs_dir)

# 使用第一张GPU卡
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def print_image():
    # 测试图片是否正确
    print(train_cat_fnames[:10])
    print(train_dog_fnames[:10])

    print('total training cat images :', len(os.listdir(train_cats_dir)))
    print('total training dog images :', len(os.listdir(train_dogs_dir)))

    print('total validation cat images :', len(os.listdir(validation_cats_dir)))
    print('total validation dog images :', len(os.listdir(validation_dogs_dir)))


def create_model():
    # 定义模型
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    # 输出摘要
    print(model.summary())

    # 编译
    model.compile(loss='binary_crossentropy',
                  optimizer=RMSprop(lr=1e-4),
                  metrics=['acc'])
    return model


def train(model):
    # 建立图片生成器
    # All images will be rescaled by 1./255
    train_datagen = ImageDataGenerator(rescale=1. / 255)
    test_datagen = ImageDataGenerator(rescale=1. / 255)

    # Flow training images in batches of 20 using train_datagen generator
    train_generator = train_datagen.flow_from_directory(
        train_dir,  # This is the source directory for training images
        target_size=(150, 150),  # All images will be resized to 150x150
        batch_size=20,
        # Since we use binary_crossentropy loss, we need binary labels
        class_mode='binary')

    # Flow validation images in batches of 20 using test_datagen generator
    validation_generator = test_datagen.flow_from_directory(
        validation_dir,
        target_size=(150, 150),
        batch_size=20,
        class_mode='binary')

    # 训练过程
    history = model.fit(
        train_generator,
        steps_per_epoch=100,  # 2000 images = batch_size * steps
        epochs=100,
        validation_data=validation_generator,
        validation_steps=50,  # 1000 images = batch_size * steps
        verbose=2)

    print("train success")


def save_model(model):
    model_path = "tf_model.pb"
    tf.keras.models.save_model(model, model_path, overwrite=True, include_optimizer=True)


if __name__ == '__main__':
    print_image()
    model = create_model()
    train(model)
    save_model(model)
