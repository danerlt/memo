import argparse
import asyncio
import json
import platform
from typing import List
import os
import pandas as pd

import psycopg2
from psycopg2.extras import execute_batch
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from openai import AsyncOpenAI

from common.const import DATA_PATH
from utils.log_utils import logger

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# 加载环境变量
load_dotenv()


def create_database():
    """创建数据库（如果不存在）"""
    db_name = os.environ.get("DB_NAME")
    conn = psycopg2.connect(
        dbname="postgres",
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT")
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # 检查数据库是否存在
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
    exists = cursor.fetchone()
    if not exists:
        logger.info(f"数据库 {db_name} 不存在，需要创建数据库")
        cursor.execute(f"CREATE DATABASE {db_name}")
        logger.info(f"数据库 {db_name} 已创建")
    else:
        logger.info(f"数据库 {db_name} 已存在，无需创建数据库")

    cursor.close()
    conn.close()


def init_db():
    """初始化PostgreSQL数据库连接并创建表（如果不存在）"""
    create_database()  # 确保数据库存在

    conn = psycopg2.connect(
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT")
    )
    cursor = conn.cursor()

    # 创建表（如果不存在）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS answer (
        id SERIAL PRIMARY KEY,
        input TEXT,
        answer TEXT,
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    logger.info("数据库表已初始化")
    return conn


def get_conn():
    conn = psycopg2.connect(
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT")
    )
    return conn


def save_to_db(conn, batch_results):
    """保存结果到数据库

    :param conn:
    :param batch_results:
    :return:
    """
    logger.debug("开始保存结果到数据库")
    cursor = conn.cursor()
    sql = """
    INSERT INTO answer (input, answer)
    VALUES (%s, %s)
    """
    execute_batch(cursor,
                  sql,
                  [(input_text, answer) for input_text, answer in batch_results]
                  )
    conn.commit()
    logger.debug("保存结果到数据库成功")



async def chat(user_input: str, is_return_dict=False) -> str | dict:
    """和大模型对话

    :param user_input:
    :param is_return_dict: 是否返回dict，默认为False
    :return:
    """

    client = AsyncOpenAI(
        base_url=os.environ.get("OPENAI_API_BASE"),
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    completion = await client.chat.completions.create(
        model=os.environ.get("MODEL"),
        messages=[
            {
                "role": "user",
                "content": f"结果以json格式输出。\n{user_input}"
            }
        ]
    )

    answer = completion.choices[0].message.content
    if is_return_dict:
        json_parser = JsonOutputParser()
        answer_dict = json_parser.parse(answer)
        return answer_dict
    else:
        return answer


def parse_args():
    """解析命令行参数

    :return:
    """
    logger.info("开始解析命令行参数")
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",
                        "--input-file",
                        required=True,
                        type=str,
                        help="大模型对话输入文件路径")
    parser.add_argument("-b",
                        "--batch-size",
                        type=int,
                        default=32,
                        help="批处理大小")
    result = parser.parse_args()
    logger.info(f"命令行参数为：{result}")
    return result


def read_file(file_name: str) -> list[str]:
    logger.info(f"开始读取文件: {file_name}")
    file_path = DATA_PATH.joinpath(file_name)
    logger.info(f"文件路径: {file_path.as_posix()}")
    if file_path.suffix != ".csv":
        logger.error("只支持csv格式的文件")
        raise Exception("只支持csv格式的文件")
    df = pd.read_csv(file_path)
    process_name = df["Process Name"]
    result = process_name.values
    logger.info(f"读取文件结束，数据条数有：{len(result)}")
    return result


async def process_batch(batch_inputs: List[str]) -> List[tuple]:
    """处理一个批次的输入

    :param batch_inputs:
    :return:
    """
    tasks = [chat(input_text, is_return_dict=True) for input_text in batch_inputs]
    results = await asyncio.gather(*tasks)
    return [(input_text, json.dumps(answer, ensure_ascii=False, indent=4)) for input_text, answer in zip(batch_inputs, results)]


def filter_processed_data(conn, inputs: List[str]) -> List[str]:
    """过滤已经处理过的数据

    :param conn: 数据库连接
    :param inputs: 输入数据列表
    :return: 未处理的数据列表
    """
    logger.debug(f"开始过滤已经处理过的数据，过滤前的数据条数：{len(inputs)}")
    cursor = conn.cursor()
    placeholders = ','.join(['%s'] * len(inputs))
    query = f"SELECT input FROM answer WHERE input IN ({placeholders})"
    cursor.execute(query, inputs)
    processed_inputs = {row[0] for row in cursor.fetchall()}
    cursor.close()
    result = [input_text for input_text in inputs if input_text not in processed_inputs]
    logger.debug(f"结束过滤已经处理过的数据，过滤后的数据条数：{len(result)}")
    return result


async def main(args):
    batch_size = args.batch_size

    # 初始化数据库连接
    db_conn = init_db()

    inputs = read_file(args.input_file)
    inputs = filter_processed_data(db_conn, inputs)
    for i in range(0, len(inputs), batch_size):
        batch = inputs[i:i + batch_size]
        logger.info(f"Processing batch {i // batch_size + 1}, size: {len(batch)}")

        batch_results = await process_batch(batch)
        save_to_db(db_conn, batch_results)

    db_conn.close()
    logger.info("处理完成")


if __name__ == '__main__':
    _args = parse_args()
    asyncio.run(main(_args))
