#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: model.py 
@time: 2022-08-12
@contact: danerlt001@gmail.com
@desc: 数据库表基类
"""
import datetime
import json
from inspect import isfunction, ismethod

from common.json_encoder import OtherEncoder


class ModelBase(object):
    def __repr__(self):
        result = self.to_dict()
        return json.dumps(result, ensure_ascii=False, cls=OtherEncoder)

    def to_dict(self):
        """
        class转换为dict
        :return:
        """
        result = {}
        for key in self.__class__.__dict__.keys():
            tmp = getattr(self, key)
            if key.startswith("_") or ismethod(tmp) or isfunction(tmp):
                continue
            # 去掉relatonship字段
            if isinstance(tmp, ModelBase):
                continue
            result[key] = tmp
        return result

    def set_field(self, data=None):
        if data is None:
            data = {}
        for key in self.__class__.__dict__.keys():
            tmp = getattr(self, key)
            if key.startswith("_") or ismethod(tmp) or isfunction(tmp):
                continue
            if key in data:
                setattr(self, key, data[key])

        insert_time_keys = ["inserttime", "insert_time"]
        # 这里分开设置是因为insert_time只需要赋值一次,而update_time每次setFeild的时候都要覆盖以前的值,
        # 注意: 这里保存数据库要注意保存的时间是北京时间
        for insert_time_key in insert_time_keys:
            if hasattr(self, insert_time_key):
                old_insert_time = getattr(self, insert_time_key)
                if old_insert_time in [None, ""]:
                    # 判断insert_time有没有初始化
                    setattr(self, insert_time_key, datetime.datetime.now())
        # 设置update_time
        update_time_keys = ["updatetime", "update_time"]
        for update_time_key in update_time_keys:
            if hasattr(self, update_time_key):
                setattr(self, update_time_key, datetime.datetime.now())
