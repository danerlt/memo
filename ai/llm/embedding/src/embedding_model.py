#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
from pathlib import Path

import torch
from sentence_transformers import SentenceTransformer

from const import DEFAULT_MODEL_NAME, MODELS_PATH
from errors import ModelException

logger = logging.getLogger("model")


class EmbeddingModel(object):
    def __init__(
        self, models_path: str = MODELS_PATH, model_name: str = DEFAULT_MODEL_NAME
    ):
        """初始化 EmbeddingModel

        Args:
            models_path (str): models目录路径
            model_name (str): 模型名称,也就是models目录下的子目录名称
        """
        logger.info(f"使用模型:{model_name}")
        self.model_name = model_name

        p_models_path = Path(models_path)
        if not p_models_path.exists():
            raise ModelException(f"{models_path}目录不存在")
        p_model_path = p_models_path.joinpath(model_name)
        if not p_model_path.exists():
            raise ModelException(f"模型: {model_name} 目录不存在,请检查")
        self.model_path = str(p_model_path)

        device = self.infer_torch_device()

        self.model = SentenceTransformer(self.model_path, device=device)

    def infer_torch_device(self):
        has_cuda = torch.cuda.is_available()
        if has_cuda:
            return "cuda"
        return "cpu"


embedding_model = EmbeddingModel()
