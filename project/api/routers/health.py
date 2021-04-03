# -*- coding: utf-8 -*-

from fastapi import APIRouter


health_router = APIRouter()


@health_router.get("/ping")
def ping():
    return {"result": "pong"}
