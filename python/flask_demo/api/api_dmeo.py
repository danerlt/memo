#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt
@file: api_dmeo.py 
@time: 2023-01-06
@contact: danerlt001@gmail.com
@desc: 
"""
from flask import jsonify

from common.app import app

from uitls.logutil import creater_logger
from service.service_demo import demo_service

logger = creater_logger("api")


@app.route("/demo", methods=["GET"])
def demo():
    result = {"code": 0, "msg": "success"}
    try:
        data = demo_service()
        result["data"] = data
    except Exception as e:
        logger.exception(str(e))
        result["code"] = 1000
        result["msg"] = str(e)

    return jsonify(**result)
