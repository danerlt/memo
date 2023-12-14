#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: mnist.py 
@time: 2023-12-14
@contact: danerlt001@gmail.com
@desc: 
"""
import time

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from loguru import logger

logger.add("mnist.log")


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


def get_data_loader(is_train=True, batch_size=64):
    """ 获取data_loader
    :param is_train: 是否是训练
    :param batch_size: 批次数量
    :return:
    """
    transforms_compose = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    data = datasets.MNIST('data', train=is_train, download=True, transform=transforms_compose)
    data_loader = DataLoader(data, batch_size=batch_size, shuffle=is_train)
    return data_loader


def train(device, model, train_loader=None, test_loader=None, epochs=15):
    """ 训练代码
    :param device:
    :param model:
    :param train_loader:
    :param test_loader:
    :param epochs:
    :return:
    """
    logger.info(f"开始在设备 {device} 上训练")
    start_time = time.perf_counter()
    optimizer = optim.Adam(model.parameters())
    for epoch in range(1, epochs + 1):
        model.train()
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss = F.nll_loss(output, target)
            loss.backward()
            optimizer.step()

        loss, acc = test(device, model, test_loader=test_loader)
        logger.debug(f"Epoch: {epoch}, loss: {loss}, acc: {acc:.2f}%")

    end_time = time.perf_counter()
    logger.info(f"在设备 {device} 上训练结束，耗时 {round(end_time - start_time, 2)}秒")


def test(device, model, test_loader=None):
    """测试

    :param model:
    :param device:
    :param test_loader:
    :return:
    """
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            logger.debug(f"output type: {type(output)}, shape: {output.shape}, output: {output}")
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # 将一批的损失相加
            pred = output.max(1, keepdim=True)[1]  # 找到概率最大的下标
            logger.debug(f"pred type: {type(pred)}, shape: {pred.shape}, pred: {pred}")
            correct += pred.eq(target.view_as(pred)).sum().item()
            logger.debug(f"correct type: {type(correct)}, correct: {correct}")

    loss = test_loss / len(test_loader.dataset)
    acc = 100. * correct / len(test_loader.dataset)
    return loss, acc


def main():
    logger.info("程序开始")
    start_time = time.perf_counter()
    batch_size = 5  # 大概需要2G的显存
    epochs = 5  # 总共训练批次
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 让torch判断是否使用GPU，建议使用GPU环境，因为会快很多

    model = ConvNet().to(device)

    train_loader = get_data_loader(is_train=True, batch_size=batch_size)
    test_loader = get_data_loader(is_train=False, batch_size=batch_size)
    train(device, model, train_loader=train_loader, test_loader=test_loader, epochs=epochs)
    end_time = time.perf_counter()
    logger.info(f"程序结束, 总执行耗时： {round(end_time - start_time, 2)}秒")


if __name__ == '__main__':
    main()
