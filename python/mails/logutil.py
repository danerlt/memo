import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

logger_level = logging.INFO

LOG_DIR_PATH = Path(__file__).parent.joinpath("logs")

if not LOG_DIR_PATH.exists():
    LOG_DIR_PATH.mkdir()


def create_logger(name=None):
    if name:
        log_file = name + ".log"
        _logger = logging.Logger.manager.getLogger(name)
    else:
        log_file = "app.log"
        _logger = logging.RootLogger(logger_level)

    # 设置日志级别
    _logger.setLevel(logger_level)
    # 设置第三方库为ERROR级别
    only_error_loggers = ["apscheduler", "pika"]
    for err_logger in only_error_loggers:
        if name and err_logger in name:
            _logger.setLevel(logging.ERROR)

    # 定义日志格式
    format_str = '%(asctime)s %(levelname)s [%(filename)s.py %(lineno)d %(funcName)s] %(message)s'
    formatter = logging.Formatter(format_str)

    # 添加打印到控制台的handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # 添加记录到日志文件的handler
    # 用于记录到文件的处理程序，以特定的时间间隔轮换日志文件。如果 backupCount > 0，则在完成翻转后，
    # 将保留不超过 backupCount 个文件, 最旧的文件将被删除。
    # 日志轮转的单位 默认为D 表示天  S：秒 M：分钟 H：小时 D：天
    when = "D"
    # 日志轮转的间隔 默认7天
    interval = 7
    # 已经轮转的日志文件最大保留个数 默认30天
    backup_cunt = 30
    log_file_path = LOG_DIR_PATH.joinpath(log_file)
    file_handler = TimedRotatingFileHandler(log_file_path,
                                            when=when,
                                            interval=interval,
                                            backupCount=backup_cunt,
                                            encoding='utf-8')
    file_handler.setFormatter(formatter)

    _logger.addHandler(console_handler)
    _logger.addHandler(file_handler)
    return _logger


logger = create_logger()
