#!/usr/bin/env python
# -*- coding:utf-8 -*-  
""" 
@author: danerlt
@file: config.py 
@time: 2023-04-01
@contact: danerlt001@gmail.com
@des: 数据库配置
"""

from dataclasses import dataclass


@dataclass
class Config(object):
    pass


@dataclass
class MysqlConfig(Config):
    host: str
    user: str
    password: str
    db: str
    port: int = 3306
    charset: str = "utf8mb4"

    def get_uri(self):
        return f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}?charset={self.charset}"


# MySQL配置
mysql_config = MysqlConfig(host="my_host",
                           user="root",
                           password="123456",
                           db="my_db",
                           port=3306)
