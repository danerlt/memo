# base image
FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04 AS base

LABEL maintainer="danerlt001@gmail.com"

# 使用 root 用户
USER root

# 设置环境变量
# 防止 python 将 pyc 文件写入硬盘
ENV PYTHONDONTWRITEBYTECODE 1
# 防止 python 缓冲 (buffering) stdout 和 stderr, 以便更容易地进行容器日志记录
ENV PYTHONUNBUFFERED 1
# 设置pip安装命令
ENV PIP_INSTALL="pip3 install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple/"

# 设置apt源
COPY sources.list /etc/apt/
# 安装apt依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends libc-dev net-tools wget curl vim python3.10 python3-pip \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*


# 拷贝python依赖
COPY requirements.txt /requirements.txt
# 安装python依赖
RUN  ${PIP_INSTALL} -r /requirements.txt


# set timezone
ENV TZ UTC
ENV PORT 8077
ENV MODEL_NAME ""

WORKDIR /app
COPY start.sh /app/start.sh
COPY supervisord.conf /app/supervisord.conf
RUN chmod +x /app/start.sh

EXPOSE $PORT

CMD ["/bin/bash", "/app/start.sh"]