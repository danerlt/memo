#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt 
@file: mult_thread_save.py 
@time: 2023-04-24
@contact: danerlt001@gmail.com
@desc: 多线程批量写入数据库样例
"""

import time
import profile

from multiprocessing.dummy import Pool

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from config import mysql_config

from logutil import creater_logger

logger = creater_logger()

engine = create_engine(mysql_config.get_uri(),
                       pool_size=30,
                       max_overflow=0,
                       pool_timeout=30,
                       pool_recycle=-1
                       )
Session = sessionmaker(bind=engine)


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        use_time = round(end_time - start_time, 2)
        logger.info(f"函数 {func.__name__} 的执行时间为 {use_time} 秒。")
        return result

    return wrapper


def save_db(session, data_list: list):
    """保存数据到数据库
    :param session
    :param data_list
    """
    try:
        for data in data_list:
            sql = data["sql"]
            sql_data = data["sql_data"]
            sql_2 = data["sql_2"]
            data_2 = data["data_2"]

            res = session.execute(sql, sql_data)
            if res.rowcount > 0:
                logger.info("插入tabel1表成功")
            else:
                msg = "插入table1表失败"
                logger.error(msg)
                raise Exception(msg)

            res = session.execute(sql_2, data_2)
            if res.rowcount > 0:
                logger.info("插入table2表成功")
            else:
                msg = "插入table2表成功"
                logger.error(msg)
                raise Exception(msg)

        session.commit()
        logger.info("提交数据库事务成功")
    except Exception as e:
        logger.error(f"执行SQL失败, error:{e}")
        session.rollback()
        raise e


@timer
def get_save_db_list():
    """获取保存到数据库的数据"""
    logger.info("开始获取保存到数据库的数据")

    result = []
    for i in range(10):
        table_id = i + 1
        name = "tttt"

        sql = text("""
            INSERT INTO table1 (id, name)
            VALUES (:table_id, :name)
        """)
        sql_data = {
            "id": table_id,
            "name": name,

        }
        sql_2 = text("""
            INSERT INTO table2 (id2, name2)
            VALUES (:table_id2, :name2)
        """)
        sql_2_data = []
        for _ in range(3):
            name2 = "xxxx"
            row = {
                "id2": table_id,
                "name2": name2,
            }
            sql_2_data.append(row)

        item = {
            "sql": sql,
            "data": sql_data,
            "sql_2": sql_2,
            "data_2": sql_2_data,
        }
        result.append(item)

    logger.info(f"获取保存到数据库的数据成功, 共有 {len(result)} 条数据")
    return result


@timer
def split_data(data, batch_size):
    data_blocks = [data[i:i + batch_size] for i in range(0, len(data), batch_size)]
    return data_blocks


def write_data_using_threads(data):
    """使用多线程插入数据"""
    NUM_THREADS = 8  # 定义线程数量
    BATCH_SIZE = 100  # 每个线程处理的数据大小

    # 将数据块进行拆分
    data_blocks = list(split_data(data, BATCH_SIZE))

    # 创建线程池
    pool = Pool(NUM_THREADS)

    # 在每个线程中执行数据插入操作
    for data_block in data_blocks:
        session = Session()
        pool.apply_async(save_db, args=(session, data_block))

    # 关闭线程池并等待所有线程操作完成
    pool.close()
    pool.join()


@timer
def main():
    save_db_list = get_save_db_list()
    write_data_using_threads(save_db_list)


if __name__ == '__main__':
    main()

# 使用profile分析代码执行时间
# profile.run('main()')
