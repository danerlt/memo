#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: main.py 
@time: 2022-10-16
@contact: danerlt001@gmail.com
@desc: 
"""

from common.app import app


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == '__main__':
    main()
