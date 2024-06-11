# base image
FROM python:3.10-slim-bookworm AS base

# 设置apt源
COPY build/sources.list /etc/apt/

LABEL maintainer="danerlt001@gmail.com"

# install packages
FROM base AS packages

# pip 环境变量
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_INSTALL="pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple/ "

# 安装apt依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ libc-dev libffi-dev libgmp-dev libmpfr-dev libmpc-dev


# 安装依赖
COPY build /build
# --mount 参数会提示 buildx 缓存 /root/.cache 以加速下一次构建
RUN --mount=type=cache,target=/root/.cache/pip \
    cd /build \
    && ${PIP_INSTALL} --prefix=/pkg -r requirements.txt


FROM base AS production
# 使用 root 用户
USER root

# 设置环境变量
# 防止 python 将 pyc 文件写入硬盘
ENV PYTHONDONTWRITEBYTECODE=1
# 防止 python 缓冲 (buffering) stdout 和 stderr, 以便更容易地进行容器日志记录
ENV PYTHONUNBUFFERED=1
# 设置时区
ENV TZ=UTC

# 安装apt依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends wget curl vim nginx postgresql-client \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*


# 拷贝Python依赖
COPY --from=packages /pkg /usr/local

# 设置项目文件
WORKDIR /app
ENV PYTHONPATH="/app:$PYTHONPATH"

# 拷贝项目文件
COPY src /app
COPY run /app/run

# 设置nginx和清空日志
RUN rm /etc/nginx/sites-enabled/default \
    && cp /app/run/nginx.conf /etc/nginx/sites-available/app.conf \
    && mkdir -p /app/logs \
    && find /app/logs -name "*.log" -exec sh -c '> "{}"'   \;

EXPOSE 8000

CMD ["bash", "/app/run/start.sh"]

