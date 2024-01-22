#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: danerlt
@file: bert.py
@time: 2023-12-13
@contact: danerlt001@gmail.com
@desc: Bert 文本分类模型  单机单卡训练
"""
import re
import time
import typing as t

import numpy as np
import torch
import torch.optim as optim
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from transformers import BertForSequenceClassification
from transformers import BertTokenizer

from common import const
from utils.logging import get_logger

logger = get_logger("bert")


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
    bert_name = 'bert-base-uncased'
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
                    batch_size: int = 64) -> t.Tuple[DataLoader, DataLoader]:
    """获取训练和测试的data_loader

    :param positive_data_file:
    :param negative_data_file:
    :param batch_size: 批次大小
    :return: (train_loader, test_loader)
    """
    x_text, y = load_data_and_labels(positive_data_file, negative_data_file)
    x_train, x_test, y_train, y_test = train_test_split(x_text,
                                                        y,
                                                        test_size=0.1)
    train_data = Data(x_train, y_train)
    test_data = Data(x_test, y_test)
    train_loader = DataLoader(train_data,
                              batch_size=batch_size,
                              collate_fn=collate_fn)
    test_loader = DataLoader(test_data,
                             batch_size=batch_size,
                             shuffle=False,
                             collate_fn=collate_fn)
    return train_loader, test_loader


def train(device, train_loader, test_loader, epochs=15, lr=2e-5):
    """训练函数

    :param device
    :param train_loader
    :param test_loader
    :param epochs: 训练批次
    :param lr:
    """
    logger.info("开始训练")
    start_train_time = time.perf_counter()

    # 加载预训练模型并且移动到GPU上
    model_path = './bert-base-uncased'
    model = BertForSequenceClassification.from_pretrained(model_path,
                                                          num_labels=2)
    model.to(device)

    optimizer = optim.Adam(model.parameters(), lr=lr)
    best_acc = -0.1
    for epoch in range(1, epochs + 1):
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
        logger.debug(f"Epoch: {epoch}: loss: {total_loss:.4f}, acc: {acc:.4f}")
        if acc > best_acc:
            best_acc = acc
    end_time = time.perf_counter()
    train_cost_time = round(end_time - start_train_time, 2)
    logger.info(f"结束训练，训练耗时: {train_cost_time}秒, best acc: {best_acc:.4f}%")


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
            preds.append(predict)
            labels.append(truth)

    model.train()
    predict = torch.cat(preds, 0)
    labels = torch.cat(labels, 0)
    correct = (predict == labels).sum().item()
    acc = correct * 100.0 / len(labels)
    return acc


def main():
    logger.info("启动程序")
    start_time = time.perf_counter()

    # 加载数据
    batch_size = 64
    positive_data_file = const.DATA_PATH.joinpath("rt-polarity.pos")
    negative_data_file = const.DATA_PATH.joinpath("rt-polarity.neg")
    train_loader, test_loader = get_data_loader(positive_data_file,
                                                negative_data_file,
                                                batch_size=batch_size)

    # 训练
    epochs = 15
    lr = 2e-5
    # 设置GPU 默认使用第一个GPU
    device = torch.device("cuda:0")
    torch.cuda.set_device(device)
    train(device, train_loader, test_loader, epochs=epochs, lr=lr)

    end_time = time.perf_counter()
    main_cost_time = round(end_time - start_time, 2)
    logger.info(f"总共运行耗时: {main_cost_time}秒")
    logger.info("程序结束")


if __name__ == '__main__':
    main()
