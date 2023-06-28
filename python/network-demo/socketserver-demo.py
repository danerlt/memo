#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: danerlt
@file: socketserver-demo.py
@time: 2023-06-28
@contact: danerlt001@gmail.com
@desc:
"""

import socketserver
import time
import threading
from queue import Queue, Empty

from loguru import logger as log

log.add("server.log")


class MyRequestHandler:

    def __init__(self, request, client_address, server, result_queue=None):
        """
        初始化
        :param request: 请求
        :param client_address: 客户端地址
        :param server: 服务端
        :param result_queue: 结果队列
        """
        self.request = request
        self.client_address = client_address
        self.server = server
        self.result_queue = result_queue

        log.info(f"连接到客户端: {self.client_address}")
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def setup(self):
        pass

    def handle(self):
        log.info("handle 处理")
        # 这里必须阻塞 否则会导致handle_request线程还没启动就执行了shutdown_request将request关闭了。
        self.handle_request()

    def finish(self):
        pass

    def handle_request(self):
        while True:
            try:
                # 开始接受数据
                data = self.request.recv(1024)
                if not data:
                    continue
                log.info(f"服务端收到数据: {data}")
                self.result_queue.put(data)
            except OSError:
                log.info("客户端断开连接")
                break
            except Exception as e:
                log.error(f"服务端接收数据异常: {e}")
                break


class MyTcpServer(socketserver.ThreadingTCPServer):

    def __init__(self, server_address, RequestHandlerClass, result_queue=None):
        super().__init__(server_address, RequestHandlerClass)
        log.info(f"服务端启动: {server_address}")
        self.result_queue = result_queue

    def finish_request(self, request, client_address):
        """Finish one request by instantiating RequestHandlerClass."""
        self.RequestHandlerClass(request, client_address, self, result_queue=self.result_queue)


def start_server():
    pass


def handle_queue(queue):
    while True:
        try:
            data = queue.get(timeout=1)
            log.info(f"handle_queue: {data}")
        except Empty:
            time.sleep(0.01)
        except Exception as e:
            log.error(f"handle_queue: {e}")
            break


def main():
    host = "0.0.0.0"
    port = 19999
    queue = Queue()
    my_server = MyTcpServer((host, port), MyRequestHandler, result_queue=queue)
    server_thread = threading.Thread(target=my_server.serve_forever)
    server_thread.start()
    queue_thread = threading.Thread(target=handle_queue, args=(queue,))
    queue_thread.start()


if __name__ == '__main__':
    main()
