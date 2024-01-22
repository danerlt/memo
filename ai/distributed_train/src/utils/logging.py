#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: logging.py
@time: 2023-12-20
@contact: danerlt001@gmail.com
@desc: 
"""
import inspect
import logging
import os
import sys
import typing as t
import warnings
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from common import const

root_path: Path = const.ROOT_PATH
logger_dir_name = "logs"
logdir = root_path.joinpath(logger_dir_name)  # 项目日志目录


def _get_log_level() -> str:
    """
    Return default log level.
    """
    return "INFO"


def _get_log_formatter():
    format_str = "%(asctime)s %(levelname)s [pid:%(process)d] [tid:%(thread)d] [%(filename)s.py %(lineno)d %(funcName)s] %(message)s"
    return logging.Formatter(format_str)


def _create_console_handler(level: t.Union[int, str] = logging.DEBUG):
    """
    创建控制台日志handler

    Args:
        level (int or str):日志级别 (默认值: ``logging.DEBUG``)

    Returns: logging.StreamHandler

    """
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = _get_log_formatter()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    return console_handler


def _create_file_handler(filename: str,
                         level: t.Union[int, str] = logging.DEBUG,
                         logs_dir: t.Union[str, Path] = None,
                         when: str = "D",
                         interval: int = 7,
                         backup_count: int = 30):
    """
    创建写文件日志handler
    Args:
        filename (str): 日志文件名
        logs_dir (str or Path): 日志文件目录，默认为当前目录
        level (str or int): 日志级别，默认``logging.DEBUG``
        when (str): 日志轮转的时间单位，默认为``D``,表示天
        interval (int): 日志轮转的时间，默认为``7``
        backup_count (int): 日志保留历史记录的最大数量，默认为``30``

    Returns:

    """
    if logs_dir is not None:
        if isinstance(logs_dir, (str, Path)):
            if isinstance(logs_dir, str):
                logs_dir = Path(logs_dir)
        else:
            raise Exception("logs_dir must be str or Path")
    else:
        logs_dir = Path(__file__).parent

    os.makedirs(logs_dir, exist_ok=True)
    if not filename.endswith(".log"):
        filename = filename + ".log"
    file_path = logs_dir.joinpath(filename)

    file_handler = TimedRotatingFileHandler(
        file_path,
        when=when,
        interval=interval,
        backupCount=backup_count,
        encoding='utf-8'
    )
    formatter = _get_log_formatter()
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    return file_handler


def _derive_module_name(depth: int = 1) -> t.Optional[str]:
    """
    Derives the name of the caller module from the stack frames.

    Args:
        depth: The position of the frame in the stack.
    """
    try:
        stack = inspect.stack()
        assert depth < len(stack)
        # FrameInfo is just a named tuple: (frame, filename, lineno, function, code_context, index)
        frame_info = stack[depth]

        module = inspect.getmodule(frame_info[0])
        if module:
            module_name = module.__name__
        else:
            # inspect.getmodule(frame_info[0]) does NOT work (returns None) in
            # binaries built with @mode/opt
            # return the filename (minus the .py extension) as modulename
            filename = frame_info[1]
            module_name = os.path.splitext(os.path.basename(filename))[0]
        return module_name
    except Exception as e:
        warnings.warn(
            f"Error deriving logger module name, using <None>. Exception: {e}",
            RuntimeWarning,
        )
        return None


def get_logger(name: t.Optional[str] = None,
               level: t.Union[str, int] = None,
               add_console_handler: bool = True,
               add_file_handler: bool = True,
               **kwargs):
    """
    Get logger

    Args:
        name (str, optinal): logger name
        level: (str or int): 日志级别，默认为 ``logging.INFO``
        add_console_handler: 是否将日志写入到控制台
        add_file_handler (bool): 是否将日志写入到日志文件
        **kwargs: 写入日志日志文件中的关键字参数

    Returns: logging.Logger

    """
    if name is None:
        name = _derive_module_name(depth=2)
    log = logging.getLogger(name)
    if level is None:
        level = os.environ.get("LOGLEVEL", _get_log_level())
    log.setLevel(level)

    if add_console_handler:
        console_handler = _create_console_handler(level=level)
        log.addHandler(console_handler)
    if add_file_handler:
        filename = kwargs.get("filename") or name
        logs_dir = kwargs.get("logs_dir") or const.LOG_PATH
        file_handler = _create_file_handler(filename=filename, level=level, logs_dir=logs_dir, **kwargs)
        log.addHandler(file_handler)
    return log
