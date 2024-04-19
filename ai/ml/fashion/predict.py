#!/usr/bin/env python  
# -*- coding:utf-8 -*-  

from flask import Flask
from dataclasses import dataclass

app = Flask(__name__)


@dataclass
class A(object):
    name: str
    unit_price: float
    quantity_on_hand: int = 0


@app.route("/predict", methods=["POST"])
def predict():
    try:
        print(3)
    except Exception as e:
        print(e)
