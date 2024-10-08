# 3.10表示Python版本
# slim 表示精简版 大约130M，完整的Python镜像大约900M
# bookworm 是Debian  12版本的名称
# Python 分阶段构建带来的提交提示不大，可以直接使用一个镜像就可。
FROM python:3.10-slim-bookworm


ARG PIP3_INSTALL="pip3 install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple/ "
# 使用 root 用户
USER root

# 设置环境变量
# 防止 python 将 pyc 文件写入硬盘
ENV PYTHONDONTWRITEBYTECODE 1
# 防止 python 缓冲 (buffering) stdout 和 stderr, 以便更容易地进行容器日志记录
ENV PYTHONUNBUFFERED 1

# 设置apt源 如果没有这个文件，需要将下面的操作删除或注释
COPY sources.list /etc/apt/

# 安装基础软件
RUN rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && apt-get update --fix-missing \
    && apt-get -yq dist-upgrade \
    && apt-get install -y --no-install-recommends \
        locales \
        curl \
        vim \
        wget \
        net-tools \
        nginx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 设置时区和语言
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen

# 拷贝Python依赖
COPY ./requirements.txt /requirements.txt

# 安装Python依赖
RUN $PIP3_INSTALL -r /requirements.txt

# 设置工作目录
WORKDIR /app
COPY ./src /app
COPY ./run /app/run

# 设置端口
EXPOSE 8000

# 启动脚本
CMD ["sh", "/app/run/start.sh"]