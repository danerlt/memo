#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" 
@author: danerlt
@file: mnist.py
@time: 2023-12-13
@contact: danerlt001@gmail.com
@desc: MNIST数据集手写数字识别样例
"""
import time

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from common import const
from utils.logging import get_logger

logger = get_logger("mnist")


class ConvNet(nn.Module):

    def __init__(self):
        super().__init__()
        # 1,28x28
        self.conv1 = nn.Conv2d(1, 10, 5)  # 10, 24x24
        self.conv2 = nn.Conv2d(10, 20, 3)  # 128, 10x10
        self.fc1 = nn.Linear(20 * 10 * 10, 500)
        self.fc2 = nn.Linear(500, 10)

    def forward(self, x):
        in_size = x.size(0)
        out = self.conv1(x)  # 24
        out = F.relu(out)
        out = F.max_pool2d(out, 2, 2)  # 12
        out = self.conv2(out)  # 10
        out = F.relu(out)
        out = out.view(in_size, -1)
        out = self.fc1(out)
        out = F.relu(out)
        out = self.fc2(out)
        out = F.log_softmax(out, dim=1)
        return out


def train(device, train_loader, test_loader, epochs=15):
    """训练

    :param device: 设备
    :param train_loader: 训练数据 data_loader
    :param test_loader: 测试数据 data_loader
    :param epochs: 训练批次
    :return:
    """
    logger.info("开始训练")
    start_train_time = time.perf_counter()

    # 定义模型并且移动到GPU上
    model = ConvNet()
    model.to(device)

    optimizer = optim.Adam(model.parameters())
    best_acc = -0.1
    for epoch in range(1, epochs + 1):
        total_loss = 0.0
        model.train()
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss = F.nll_loss(output, target)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        acc = test(device, model, test_loader)
        logger.debug(f"Epoch: {epoch}: loss: {total_loss:.4f}, acc: {acc:.4f}")
        if acc > best_acc:
            best_acc = acc
    end_time = time.perf_counter()
    train_cost_time = round(end_time - start_train_time, 2)
    logger.info(f"结束训练，训练耗时: {train_cost_time}秒, best acc: {best_acc:.4f}%")


def test(device, model, test_loader):
    """测试

    :param device:
    :param model:
    :param test_loader:
    :return:
    """
    model.eval()
    total_corrent = 0
    total_data_num = len(test_loader.dataset)  # 测试集的总数量
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)  # batch * 10
            pred = output.max(1, keepdim=True)[1]  # 找到概率最大的下标 # batch * 1
            correct = pred.eq(target.view_as(pred)).sum().item()  # 正确的数量
            total_corrent += correct
    acc = 100. * total_corrent / total_data_num
    return acc


def get_data_loader(is_train: bool = True,
                    shuffle: bool = True,
                    batch_size: int = 512,
                    data_root_path="data") -> DataLoader:
    """获取data_loader

    :param is_train: 是否是训练集， True：训练集 False: 测试集
    :param shuffle: 是否打乱顺序
    :param batch_size: 批次大小
    :param data_root_path: 数据根目录
    :return: (train_loader, test_loader)
    """
    data_transform = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize((0.1307,), (0.3081,))])

    data = datasets.MNIST(data_root_path, train=is_train, transform=data_transform, download=True)
    data_loader = DataLoader(data, batch_size=batch_size, shuffle=shuffle)

    return data_loader


def main():
    logger.info("启动程序")
    start_time = time.perf_counter()

    # 加载数据
    batch_size = 512
    data_root_path = const.DATA_PATH
    train_loader = get_data_loader(is_train=True,
                                   shuffle=True,
                                   batch_size=batch_size,
                                   data_root_path=data_root_path)
    test_loader = get_data_loader(is_train=False,
                                  shuffle=False,
                                  batch_size=batch_size,
                                  data_root_path=data_root_path)

    # 训练
    epochs = 15
    # 设置GPU 默认使用第一个GPU
    device = torch.device("cuda:0")
    torch.cuda.set_device(device)
    train(device, train_loader, test_loader, epochs=epochs)

    end_time = time.perf_counter()
    main_cost_time = round(end_time - start_time, 2)
    logger.info(f"总共运行耗时: {main_cost_time}秒")
    logger.info("程序结束")


if __name__ == '__main__':
    main()
