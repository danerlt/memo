# 嵌入（embedding)服务

构建Docker镜像命令：

```bash
docker-compose build
```

构建完镜像大小大约在 5GB 左右。

启动服务之前需要先将 embedding 模型文件放到服务器 `/data/models` 目录下，或者修改 `docker-compose.yml` 中的 `volumes`
配置项，将`/data/models:/data/models`修改为`your dir:/data/models`。

默认情况下使用的 embedding-model 为 `m3e-base`，如果要使用其他模型，请修改 `docker-compose.yml` 中的 `environment` 配置项。

启动服务命令：

```bash
docker-compose up -d
```

## embedding接口

url: `http://ip:port/embed`

请求方式： POST

请求参数说明：

body必须是JSON，query是一个列表，其中每个元素是一个字符串，表示一个查询语句。

```json
{
  "query": [
    "用户输入的查询语句"
  ]
}
```

请求参数示例，返回格式兼容 OPENAI API ：

```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [],
      "index": 0
    }
  ],
  "model": "m3-base",
  "usage": {
    "prompt_tokens": 11,
    "total_tokens": 11
  }
}
```
