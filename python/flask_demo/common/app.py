#!/usr/bin/env python
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: app.py 
@time: 2022-10-16
@contact: danerlt001@gmail.com
@desc: 
"""

from flask import Flask

flask_name = "flask_demo"
app = Flask(flask_name)


@app.route("/", methods=["GET"])
def index():
    return "This is index"


@app.route('/health')
def health():
    return "health"
