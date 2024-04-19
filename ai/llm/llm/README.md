# LLM服务

默认情况下，服务不会将模型封装到Docker镜像中，通过挂载目录的方式，将模型文件挂载到服务容器中，从而实现模型的热更新。

构建Docker镜像命令：

```bash
docker-compose build
```

启动服务之前需要先安装 `nvidia-container-toolkit`

```bash
# centos7 安装 nvidia-container-toolkit
curl https://nvidia.github.io/nvidia-docker/centos7/nvidia-docker.repo > /etc/yum.repos.d/nvidia-docker.repo
yum -y install nvidia-container-toolkit
```

启动服务之前需要先将模型文件放到服务器 `/data/models` 目录下，或者修改 `docker-compose.yml` 中的 `volumes` 配置项，将`/data/models:/data/models`修改为`your dir:/data/models`。

启动服务命令：

```bash
docker-compose up -d
```

查看日志：

```bash
# 查看 openai_api 的日志
tail -f logs/openai_api.log
# 查看 controller 日志
tail -f logs/controller.log 
# 查看 qwen 的日志
tail -f logs/qwen.log
```

服务启动后可以通过 `http://ip:8077/` 来访问 openai api 服务。
