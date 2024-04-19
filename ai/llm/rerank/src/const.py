#!/usr/bin/env python  
# -*- coding:utf-8 -*-  

import os

MODELS_PATH = "/data/models"
DEFAULT_MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME", "bge-reranker-base")
MODEL_NAME = os.getenv("MODEL_NAME")
MAX_LENGTH = int(os.getenv("MAX_LENGTH", 512))
