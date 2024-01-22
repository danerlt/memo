#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: litao
@file: bert_ddp.py
@time: 2023-12-13
@contact: tao.li67@geely.com
@desc: Bert 文本分类模型  分布式训练
"""
import os
import re
import time
import typing as t

import numpy as np
import torch
import torch.distributed as dist
import torch.optim as optim
from sklearn.model_selection import train_test_split
from torch.nn.parallel import DistributedDataParallel
from torch.utils.data import DataLoader, DistributedSampler
from torch.utils.data import Dataset
from transformers import BertForSequenceClassification
from transformers import BertTokenizer

from common import const
from utils.logging import get_logger

logger = get_logger("bert_ddp")


class Data(Dataset):

    def __init__(self, x, y):
        self.data = list(zip(x, y))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        assert idx < len(self)
        return self.data[idx]


def now():
    return str(time.strftime('%Y-%m-%d %H:%M:%S'))


def collate_fn(batch):
    bert_name = const.DATA_PATH.joinpath("bert-base-uncased")
    bert_tokenizer = BertTokenizer.from_pretrained(bert_name)
    data, labels = zip(*batch)
    inputs = bert_tokenizer(list(data), padding=True, return_tensors='pt')
    labels = torch.tensor(labels, dtype=torch.long)
    return inputs, labels


def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def load_data_and_labels(positive_data_file, negative_data_file):
    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    # Load data from files
    positive_examples = list(
        open(positive_data_file, "r", encoding='utf-8').readlines())
    positive_examples = [s.strip() for s in positive_examples]
    negative_examples = list(
        open(negative_data_file, "r", encoding='utf-8').readlines())
    negative_examples = [s.strip() for s in negative_examples]
    # Split by words
    x_text = positive_examples + negative_examples
    x_text = [clean_str(sent) for sent in x_text]
    # x_text = list(map(lambda x: x.split(), x_text))
    # Generate labels
    positive_labels = [1 for _ in positive_examples]
    negative_labels = [0 for _ in negative_examples]
    y = np.array(positive_labels + negative_labels)
    return [x_text, y]


def get_data_loader(positive_data_file,
                    negative_data_file,
                    batch_size: int = 64) -> t.Tuple[DataLoader, DataLoader, DistributedSampler, DistributedSampler]:
    """获取训练和测试的data_loader

    :param positive_data_file:
    :param negative_data_file:
    :param batch_size: 批次大小
    :return: (train_loader, test_loader, train_dist_sampler, test_dist_sampler)
    """
    x_text, y = load_data_and_labels(positive_data_file, negative_data_file)
    x_train, x_test, y_train, y_test = train_test_split(x_text,
                                                        y,
                                                        test_size=0.1)
    train_data = Data(x_train, y_train)
    test_data = Data(x_test, y_test)
    train_dist_sampler = DistributedSampler(train_data)
    test_dist_sampler = DistributedSampler(test_data)
    # 注意: sampler和shuffle=True参数是互斥的, 这里不要加shuffle=True
    train_loader = DataLoader(train_data,
                              batch_size=batch_size,
                              collate_fn=collate_fn,
                              sampler=train_dist_sampler)
    test_loader = DataLoader(test_data,
                             batch_size=batch_size,
                             collate_fn=collate_fn,
                             sampler=test_dist_sampler)
    return train_loader, test_loader, train_dist_sampler, test_dist_sampler


def train(device, model, train_loader=None, test_loader=None, train_sampler=None, epochs=15, lr=2e-5, rank=None):
    """训练

    :param device: 设备
    :param model: 模型
    :param train_loader: 训练数据 data_loader
    :param test_loader: 测试数据 data_loader
    :param train_sampler: 训练数据 train_sampler
    :param epochs: 训练批次
    :param lr:
    :param rank: 当前进程序号
    :return:
    """
    logger.info(f"进程: {rank} 开始训练")
    start_train_time = time.perf_counter()

    # 这里将model 使用DistributedDataParallel包装
    model = DistributedDataParallel(model, device_ids=[device])

    optimizer = optim.Adam(model.parameters(), lr=lr)
    best_acc = -0.1
    for epoch in range(1, epochs + 1):
        # 注意：分布式训练的时候 每一个 epoch 都要重新设置随机种子
        train_sampler.set_epoch(epoch)
        total_loss = 0.0
        model.train()
        for step, batch_data in enumerate(train_loader):
            inputs, labels = batch_data
            inputs = inputs.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            output = model(**inputs, labels=labels)
            loss = output[0]
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        acc = test(device, model, test_loader)
        logger.debug(
            f"进程: {rank}, Epoch: {epoch}: loss: {total_loss:.4f}, acc: {acc:.4f}"
        )
        if acc > best_acc:
            best_acc = acc
    end_time = time.perf_counter()
    train_cost_time = round(end_time - start_train_time, 2)
    logger.info(
        f"进程: {rank} 结束训练, 训练耗时: {train_cost_time}秒, best acc: {best_acc:.4f}%"
    )


def test(device, model, test_loader):
    """测试模型

    :param device:
    :param model:
    :param test_loader:
    :return:
    """
    model.eval()
    preds = []
    labels = []
    with torch.no_grad():
        for data in test_loader:
            inputs, truth = data
            inputs = inputs.to(device)
            truth = truth.to(device)
            output = model(**inputs)['logits']
            predict = torch.max(output.data, 1)[1]

            cur_preds = [
                torch.ones_like(predict) for _ in range(dist.get_world_size())
            ]
            cur_truth = [
                torch.ones_like(truth) for _ in range(dist.get_world_size())
            ]
            dist.all_gather(cur_preds, predict)
            dist.all_gather(cur_truth, truth)

            preds.extend(cur_preds)
            labels.extend(cur_truth)

    model.train()
    predict = torch.cat(preds, 0)
    labels = torch.cat(labels, 0)
    correct = (predict == labels).sum().item()
    acc = correct * 100.0 / len(labels)
    return acc


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
    start_time = time.perf_counter()

    # 设置默认环境变量
    set_default_envs()

    # 初始化分布式进程组
    dist.init_process_group(backend='nccl', init_method='env://')
    size = dist.get_world_size()  # 获取进程组的大小
    rank = dist.get_rank()  # 获取当前进程在进程组的编号 全局进程ID
    local_rank = int(os.environ['LOCAL_RANK'])  # 某个节点上的进程编号

    # 加载数据
    batch_size = 64
    positive_data_file = const.DATA_PATH.joinpath("rt-polarity.pos")
    negative_data_file = const.DATA_PATH.joinpath("rt-polarity.neg")
    train_loader, test_loader, train_sampler, _ = get_data_loader(positive_data_file,
                                                                  negative_data_file,
                                                                  batch_size=batch_size)

    # 设置device
    # DDP的官方最佳实践是，每一张卡对应一个单独的GPU。所以一般情况下，通过local_rank作为当前进程GPU的id。
    device_id = local_rank
    device = torch.device(f"cuda:{device_id}")
    torch.cuda.set_device(device)

    # 加载预训练模型并且移动到GPU上
    model_path = const.DATA_PATH.joinpath("bert-base-uncased")
    model = BertForSequenceClassification.from_pretrained(model_path, num_labels=2)
    model.to(device)

    # 训练
    epochs = 15
    lr = 2e-5 * size  # 注意 这个地方的lr要乘以进程数
    train(device, model,
          train_loader=train_loader,
          test_loader=test_loader,
          train_sampler=train_sampler,
          epochs=epochs,
          lr=lr,
          rank=rank)

    end_time = time.perf_counter()
    main_cost_time = round(end_time - start_time, 2)
    logger.info(f"总共运行耗时: {main_cost_time}秒")
    logger.info("程序结束")


if __name__ == '__main__':
    main()
