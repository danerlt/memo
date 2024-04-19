# 重排（rerank)服务

构建Docker镜像命令：

```bash
docker-compose build
```

启动服务之前需要先将 rerank 模型文件放到服务器 `/data/models` 目录下，或者修改 `docker-compose.yml` 中的 `volumes` 配置项，将`/data/models:/data/models`修改为`your dir:/data/models`。

默认情况下使用的 rerank-model 为 `bge-reranker-base`，如果要使用其他模型，请修改 `docker-compose.yml` 中的 `environment` 配置项。

启动服务命令：

```bash
docker-compose up -d
```

在使用Gunicorn和Flask框架启动Web服务的时候，Gunicorn 默认会使用 `fork` 的方式创建进程。在调用 `rerank`接口的时候会报错`RuntimeError: Cannot re-initialize CUDA in forked subprocess. To use CUDA with multiprocessing, you must use the 'spawn' start method`。

解决办法：

- 使用uvicorn框架和fastapi框架启动，启动的时候可以制定多个进程，如果指定多个进程，GPU上会加载多次模型。参数格式如：`uvicorn main:app --host 0.0.0.0 --port 5000 --loop uvloop --workers 4`
- 或者使用Gunicorn框架启动的时候指定只启动一个进程，Gunicorn启动多个进程还是会出现上面的错误，只能指定一个进程。参数格式如：`gunicorn -w 1 -b 0.0.0.0:5000 main:app`
- 使用uwsgi框架启动，指定只启动一个进程，并且不能加上`--master参数`。uwsgi框架指定`--master`参数也会出现上面的错误，指定多个进程也会出现上面的错误。参数格式如：`uwsgi --http 0.0.0.0:5000 -p 1 -w main:app --enable-threads`


## 重排接口

url: `http://ip:port/rerank`

请求方式： POST

请求参数说明：

body必须是JSON
```json
{
    "query": "用户输入的查询语句",
    "documents": "需要重排的文档列表,列表的每个元素是一个字符串"
}
```

请求参数示例：

```json
{
    "query": "Python快速排序实现",
    "documents": [
        "快速排序是一种高效的排序算法，它的核心思想是采用分治法。在Python中，我们可以通过递归的方式来实现快速排序，选择一个元素作为基准，然后将剩余的元素分为两部分，一部分是小于基准元素的，另一部分是大于基准元素的，最后再对这两部分分别进行快速排序。",
        "Python是一种非常流行的编程语言，它简洁易读的语法使得它在数据分析、机器学习、Web开发等领域有着广泛的应用。Python还有一个强大的标准库，提供了很多方便的功能。",
        "在Python中，快速排序可以通过递归实现。首先，选择一个基准元素，然后将数组划分为两部分，一部分是小于基准元素的，另一部分是大于基准元素的。然后，再对这两部分进行快速排序。快速排序的时间复杂度为O(nlogn)。"
    ]
}
```

