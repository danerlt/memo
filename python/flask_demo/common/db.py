#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt
@file: db.py 
@time: 2022-08-11
@contact: danerlt001@gmail.com
@desc: 
"""
import logging
import os

from flask_sqlalchemy import SQLAlchemy

from common.app import app

from common.const import ROOT_PATH
from common import config

logger = logging.getLogger("run")


def get_db_url():
    """获取数据库db_url
    默认获取的是sqlite
    """
    sqlite_path = config.JOB_CONFIG.get("sqlite_path", "output")
    sqlite_name = config.JOB_CONFIG.get("sqlite_name", "app.sqlite")
    _sqlite_abs_path = os.path.join(ROOT_PATH, sqlite_path)
    sqlite_abs_path = os.path.join(_sqlite_abs_path, sqlite_name)
    db_url = f"sqlite:///{sqlite_abs_path}"
    logger.info(f"db_url: {db_url}")
    return db_url


def get_mysql_db_url():
    """获取MySQL数据库连接"""
    try:
        db_host = config.MYSQL_CONFIG["db_host"]
        db_port = config.MYSQL_CONFIG["db_port"]
        db_user = config.MYSQL_CONFIG["db_user"]
        db_pass = config.MYSQL_CONFIG["db_pass"]
        db_name = config.MYSQL_CONFIG["db_name"]
        db_url = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        return db_url
    except Exception as e:
        logger.exception("获取MySQL数据库连接错误")
        raise Exception("获取MySQL数据库连接错误")


db_uri = get_db_url()
mysql_db_url = get_mysql_db_url()
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_BINDS"] = {
    "mysql": mysql_db_url
}

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 3600
}
db = SQLAlchemy(app, session_options={"autoflush": False})
