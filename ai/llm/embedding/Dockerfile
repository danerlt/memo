# base image
FROM python:3.10-slim-bookworm

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
    && apt-get install -y --no-install-recommends wget curl vim nginx \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

# 拷贝 requirements.txt
COPY requirements.txt /requirements.txt
# 安装Python依赖
RUN ${PIP_INSTALL} -r /requirements.txt

# set timezone
ENV TZ UTC

WORKDIR /app
COPY ./src /app
COPY ./run /app/run
RUN chmod +x /app/run/start.sh

EXPOSE 8000

CMD ["/bin/bash", "/app/run/start.sh"]
