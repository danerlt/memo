#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse

import log_utils
from embedding_model import embedding_model

logger = logging.getLogger("api")

app = FastAPI()


@app.get("/health")
def health():
    return PlainTextResponse("ok")


@app.post("/embed")
async def embedding(request: Request):
    data = await request.json()
    query_list = data.get("input", None)
    embeddings = embedding_model.model.encode(query_list)
    data = []
    for i, emb in enumerate(embeddings):
        item = {
            "object": "embedding",
            "embedding": emb.astype(float).tolist(),
            "index": i
        }
        data.append(item)
    result = {
        'object': "list",
        "data": data,
        "model": embedding_model.model_name,
        "usage": {
            "prompt_tokens": 11,
            "total_tokens": 11
        }
    }
    return JSONResponse(result)


def main():
    logger.info("服务启动")
    uvicorn.run("main:app", host="0.0.0.0", port=5000, loop="uvloop", log_level="info")


if __name__ == "__main__":
    main()
