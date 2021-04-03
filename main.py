# -*- coding: utf-8 -*-

import os

from fastapi import FastAPI
from mangum import Mangum

from project import routers


def create_app(app_name: str, debug: bool = False, **kwargs):
    app_ = FastAPI(title=app_name, debug=debug, **kwargs)
    add_routers(app_)
    return app_


def add_routers(app_: FastAPI):
    for router, prefix in routers:
        app_.include_router(router, prefix=prefix)


app = create_app(
    os.environ.get("APP_NAME", "Serverless API Service"),
    debug=os.environ.get("DEBUG", False))


handler = Mangum(app)
