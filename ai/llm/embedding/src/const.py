#!/usr/bin/env python  
# -*- coding:utf-8 -*-  

import os

MODELS_PATH = "/data/models"
DEFAULT_MODEL_NAME = os.getenv("DEFAULT_MODEL_NAME", "m3e-base")
MODEL_NAME = os.getenv("MODEL_NAME")