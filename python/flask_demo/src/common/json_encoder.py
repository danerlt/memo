#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: json_encoder.py 
@time: 2022-08-12
@contact: danerlt001@gmail.com
@desc: 
"""

import json
import datetime
import decimal


class OtherEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        if isinstance(obj, datetime.timedelta):
            return str(obj)
        if isinstance(obj, bytes):
            return int.from_bytes(obj, byteorder='little')
        if isinstance(obj, decimal.Decimal):
            if obj % 1 > 0:
                return float(obj)
            else:
                return int(obj)
        return json.JSONEncoder.default(self, obj)
