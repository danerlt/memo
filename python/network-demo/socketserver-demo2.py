#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author: danerlt
@file: socketserver-demo2.py
@time: 2023-07-03
@contact: danerlt001@gmail.com
@desc: 
"""
import random
import socketserver
import time

from loguru import logger

logger.add("server.log")


class Handler(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            try:
                data = self.request.recv(1024)
                if not data:
                    continue
                client_host, client_port = self.client_address
                logger.info(f"服务端收到客户端{client_host}:{client_port}数据: {data}")
                recv_data = bytes("hello world", encoding="utf-8")
                self.request.sendall(recv_data)
            except Exception as e:
                logger.info(f"error: {e}")
                time.sleep(1)


def main():
    host = "0.0.0.0"
    port = input("请输入服务端端口号：")
    port = int(port)
    server = socketserver.ThreadingTCPServer((host, port), Handler)
    logger.info(f"服务端{host}:{port}启动成功")
    server.serve_forever()


if __name__ == '__main__':
    main()
