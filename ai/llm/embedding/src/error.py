#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging


class ApiException(Exception):

    def __init__(self, msg: str = None):
        self.msg = msg
        self.log = logging.getLogger("api")
        self.log.error(self.msg)


class ModelException(Exception):

    def __init__(self, msg: str = None):
        self.msg = msg
        self.log = logging.getLogger("model")
        self.log.error(self.msg)
