#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt
@file: client.py 
@time: 2023-06-20
@contact: danerlt001@gmail.com
@desc: tcp 客户端
"""
import random
import socket
import time

from loguru import logger


logger.add("client.log")


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            logger.info(f"客户端连接到服务端: {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"客户端连接服务端失败, error: {str(e)}")

    def disconnect(self):
        self.client_socket.close()

    def send_message(self, messages=None):
        try:
            sleep = random.randint(1, 5)

            if isinstance(messages, str):
                messages = [messages]
            for message in messages:
                message = message.strip()
                logger.info(f"客户端发送消息: {message}")
                bytes_data = message.encode('utf-8')
                hex_bytes = bytes.fromhex(bytes_data.hex())
                self.client_socket.send(hex_bytes)
                time.sleep(sleep)
        except Exception as e:
            logger.error(f"客户端发送消息失败, error: {str(e)}")


def main():
    host = "127.0.0.1"
    port = 19999
    client = Client(host, port)
    client.connect()
    client.send_message("hello world")


if __name__ == '__main__':
    main()
