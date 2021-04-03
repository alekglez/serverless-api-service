# -*- coding: utf-8 -*-

import os
from environs import Env

context = Env()
context.read_env(os.path.join(os.getcwd(), ".env"))

from project.api.routers.health import health_router
from project.api.routers.main import core_api


routers = [
    (health_router, "/api"),
    (core_api, "/api")
]
