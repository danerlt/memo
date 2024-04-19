#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
from pathlib import Path

import torch
from sentence_transformers import CrossEncoder

from const import MODELS_PATH, MAX_LENGTH, DEFAULT_MODEL_NAME
from errors import ModelException

logger = logging.getLogger("model")


class RerankModel(object):
    def __init__(
        self,
        models_path: str = MODELS_PATH,
        model_name: str = DEFAULT_MODEL_NAME,
        max_length: int = MAX_LENGTH,
    ):
        """初始化RerankModel

        Args:
            models_path (str): models目录路径
            model_name (str): 模型名称,也就是models目录下的子目录名称
            max_length (int): 模型max_length
        """
        logger.info(f"使用模型:{model_name}, {max_length=}")
        self.model_name = model_name

        p_models_path = Path(models_path)
        if not p_models_path.exists():
            raise ModelException(f"{models_path}目录不存在")
        p_model_path = p_models_path.joinpath(model_name)
        if not p_model_path.exists():
            raise ModelException(f"模型: {model_name} 目录不存在,请检查")
        self.model_path = str(p_model_path)

        device = self.infer_torch_device()

        self.model = CrossEncoder(
            model_name=self.model_path, max_length=max_length, device=device
        )

    def infer_torch_device(self):
        has_cuda = torch.cuda.is_available()
        if has_cuda:
            return "cuda"
        return "cpu"

    def rerank(self, query, documents):
        query_docs = [(query, doc) for doc in documents]
        scores = self.model.predict(query_docs)
        scores = [float(score) for score in scores]
        return scores


rerank_model = RerankModel()
