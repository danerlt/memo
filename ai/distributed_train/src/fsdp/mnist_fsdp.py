#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" 
@author: danerlt 
@file: mnist_fsdp.py
@time: 2023-12-13
@contact: danerlt001@gmail.com
@desc: MNIST数据集手写数字识别样例  FSDP用法
"""
import functools
import os
import time

import torch
import torch.distributed as dist
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributed.fsdp import (
    FullyShardedDataParallel as FSDP,
    CPUOffload,
)
from torch.distributed.fsdp.wrap import size_based_auto_wrap_policy
from torch.utils.data import DataLoader, DistributedSampler
from torchvision import datasets, transforms

from common import const
from utils.logging import get_logger
from utils.prof import show_all_gpu_memory

logger = get_logger("mnist_fsdp")


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


def train(device, model, train_loader=None, test_loader=None, train_sampler=None, epochs=15, rank=None):
    """训练

    :param device: 设备
    :param model: 模型
    :param train_loader: 训练数据 data_loader
    :param test_loader: 测试数据 data_loader
    :param train_sampler: 测试数据 train_sampler
    :param epochs: 训练批次
    :param rank: 当前进程序号
    :return:
    """
    logger.info(f"进程: {rank} 开始")
    show_all_gpu_memory(logger=logger, note=f"进程: {rank} 开始")

    start_train_time = time.perf_counter()
    torch.cuda.set_device(device)

    # 使用FSDP将model warp起来
    logger.info(f"进程: {rank} before fsdp")
    my_auto_wrap_policy = functools.partial(
        size_based_auto_wrap_policy, min_num_params=100
    )
    model = FSDP(model, auto_wrap_policy=my_auto_wrap_policy, cpu_offload=CPUOffload(offload_params=True))
    show_all_gpu_memory(logger=logger, note=f"进程: {rank} FSDP后")

    optimizer = optim.Adam(model.parameters())
    best_acc = -0.1

    logger.info(f"进程: {rank} 开始训练")
    for epoch in range(1, epochs + 1):
        # 注意：分布式训练的时候 每一个 epoch 都要重新设置随机种子
        show_all_gpu_memory(logger=logger, note=f"进程: {rank} 开始训练 epoch：{epoch}")
        train_sampler.set_epoch(epoch)
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
        show_all_gpu_memory(logger=logger, note=f"进程: {rank} 结束训练 epoch：{epoch}")
        acc = test(device, model, test_loader)
        logger.debug(f"进程: {rank}, Epoch: {epoch}: loss: {total_loss:.4f}, acc: {acc:.4f}")
        if acc > best_acc:
            best_acc = acc

    logger.info("*" * 20)
    end_time = time.perf_counter()
    train_cost_time = round(end_time - start_train_time, 2)
    logger.info(f"进程: {rank} 结束训练, 训练耗时: {train_cost_time}秒, best acc: {best_acc:.4f}%")
    show_all_gpu_memory(logger=logger, note=f"进程: {rank} 结束训练")


def test(device, model, test_loader):
    """测试

    :param device:
    :param model:
    :param test_loader:
    :return:
    """
    show_all_gpu_memory(logger=logger, note="开始测试")
    model.eval()
    total_correct = 0
    total_data_num = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)  # batch * 10
            pred = output.max(1, keepdim=True)[1]  # 找到概率最大的下标 # batch * 1
            correct = pred.eq(target.view_as(pred)).sum()
            total_correct += correct
            data_num = len(data)
            total_data_num += data_num
    acc = 100. * total_correct / total_data_num
    show_all_gpu_memory(logger=logger, note="结束测试")
    return acc


def get_data_loader(is_train: bool = True, batch_size: int = 512, data_root_path="data") -> DataLoader:
    """获取data_loader

    :param is_train: 是否是训练集， True：训练集 False: 测试集
    :param batch_size: 批次大小
    :param data_root_path: data根路径
    :return: (train_loader, test_loader)
    """
    data_transform = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize((0.1307,), (0.3081,))])

    data = datasets.MNIST(data_root_path, train=is_train, transform=data_transform, download=True)
    dist_sampler = DistributedSampler(data)
    data_loader = DataLoader(data, batch_size=batch_size, sampler=dist_sampler)
    return data_loader, dist_sampler


def set_default_envs():
    """设置环境变量
    """
    os.environ['LOGLEVEL'] = 'DEBUG'  # 设置pytorch的日志级别
    os.environ['NCCL_DEBUG'] = 'INFO'  # 设置nccl的日志级别
    os.environ['NCCL_IB_DISABLE'] = '1'  # 关闭NCCL的InfiniBand通信
    os.environ['NCCL_DESYNC_DEBUG'] = '1'  # 关闭NCCL的InfiniBand通信
    os.environ['NCCL_ASYNC_ERROR_HANDLING'] = '1'  # 关闭NCCL的InfiniBand通信
    os.environ["TORCH_CPP_LOG_LEVEL"] = "INFO"  # 设置torch c++的日志级别
    os.environ["TORCH_DISTRIBUTED_DEBUG"] = "DETAIL"  # 设置torch distributed的日志级别
    if not os.environ.get("NCCL_SOCKET_IFNAME"):
        os.environ['NCCL_SOCKET_IFNAME'] = 'bond0'  # 设置NCCL默认的网卡名称


def main():
    logger.info("启动程序")
    show_all_gpu_memory(logger=logger, note="启动程序")
    start_time = time.perf_counter()

    # 设置默认环境变量
    set_default_envs()

    # 初始化分布式进程组
    dist.init_process_group(backend='nccl', init_method='env://')
    rank = dist.get_rank()  # 获取当前进程在进程组的编号 全局进程ID
    local_rank = int(os.environ['LOCAL_RANK'])  # 某个节点上的进程编号

    # 加载数据
    show_all_gpu_memory(logger=logger, note="加载数据前")
    batch_size = 512
    data_root_path = const.DATA_PATH
    train_loader, train_sampler = get_data_loader(is_train=True, batch_size=batch_size, data_root_path=data_root_path)
    test_loader, _ = get_data_loader(is_train=False, batch_size=batch_size, data_root_path=data_root_path)
    show_all_gpu_memory(logger=logger, note="加载数据后")

    # 设置device
    # DDP的官方最佳实践是，每一张卡对应一个单独的GPU。所以一般情况下，通过local_rank作为当前进程GPU的id。
    device_id = local_rank
    device = torch.device(f"cuda:{device_id}")
    torch.cuda.set_device(device)

    # 定义模型并且移动到GPU上
    model = ConvNet()
    show_all_gpu_memory(logger=logger, note="定义模型后")
    model.to(device)
    show_all_gpu_memory(logger=logger, note="移动到GPU后")

    # 训练
    epochs = 15
    train(device,
          model,
          train_loader=train_loader,
          test_loader=test_loader,
          train_sampler=train_sampler,
          epochs=epochs,
          rank=rank)

    end_time = time.perf_counter()
    main_cost_time = round(end_time - start_time, 2)
    logger.info(f"总共运行耗时: {main_cost_time}秒")
    logger.info("程序结束")


if __name__ == '__main__':
    main()
