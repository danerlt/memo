# 分阶段构建
# 测试下来分阶段构建大小只少了30M，提示不大。
FROM python:3.10-slim-bookworm AS base

FROM base AS apt

COPY sources.list /etc/apt/

# 安装基础软件
RUN apt-get update --fix-missing \
    && apt-get -yq dist-upgrade \
    && apt-get install -y --no-install-recommends \
        locales \
        curl \
        vim \
        wget \
        net-tools \
        nginx

FROM base AS pip

ENV PIP3_INSTALL="pip3 install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple/ "

# 拷贝Python依赖
COPY ./requirements.txt /requirements.txt

# 安装Python依赖
RUN ${PIP3_INSTALL} --prefix=/pkg -r /requirements.txt

FROM base AS app

# 使用 root 用户
USER root

# 设置环境变量
# 防止 python 将 pyc 文件写入硬盘
ENV PYTHONDONTWRITEBYTECODE 1
# 防止 python 缓冲 (buffering) stdout 和 stderr, 以便更容易地进行容器日志记录
ENV PYTHONUNBUFFERED 1

# 拷贝依赖
COPY --from=apt /usr/bin /usr/bin
COPY --from=apt /usr/sbin /usr/sbin
COPY --from=pip /pkg /usr/local/bin/

# 设置时区和语言
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen

# 设置工作目录
WORKDIR /app
COPY ./src /app
COPY ./run /app/run

# 设置端口
EXPOSE 8000

# 启动脚本
CMD ["sh", "/app/run/start.sh"]