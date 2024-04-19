#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse

import log_utils
from rerank_model import rerank_model

logger = logging.getLogger("api")

app = FastAPI()


@app.get("/health")
def health():
    return PlainTextResponse("ok")


@app.post("/rerank")
async def rerank(request: Request):
    data = await request.json()
    query = data.get("query", None)
    documents = data.get("documents", None)
    scores = rerank_model.rerank(query, documents)
    result = {"model_name": rerank_model.model_name, "data": scores}
    return JSONResponse(result)


def main():
    logger.info("服务启动")
    uvicorn.run("main:app", host="0.0.0.0", port=5000, loop="uvloop", log_level="info")


if __name__ == "__main__":
    main()
