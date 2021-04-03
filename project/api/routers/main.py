# -*- coding: utf-8 -*-

import json
import os
from http import HTTPStatus

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from starlette.status import (
    HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT,
    HTTP_200_OK, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_405_METHOD_NOT_ALLOWED
)

from project.api.controllers.main import Controller
from project.api.services.base import ServiceException

services = os.environ.get("ACTIVE_SERVICES", "")
controller = Controller(services)
core_api = APIRouter()


@core_api.get("/{model}", status_code=HTTP_200_OK)
def get_records(request: Request, model):
    parameters = request.query_params
    filters, fields = parameters.get("filters"), parameters.get("fields"),
    offset, limit = parameters.get("offset"), parameters.get("limit", 20)

    try:
        result = controller.get_all(model, filters=filters, fields=fields, offset=offset, limit=limit)
        return JSONResponse(content=result)

    except NotImplementedError:
        return JSONResponse(status_code=HTTP_405_METHOD_NOT_ALLOWED)

    except Exception as error:
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(error)})


@core_api.get("/{model}/{record_id}", status_code=HTTP_200_OK)
def get_record(model, record_id):
    try:
        result = controller.get(model, record_id)
        return JSONResponse(content=result)

    except KeyError:
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={})

    except NotImplementedError:
        return JSONResponse(status_code=HTTP_405_METHOD_NOT_ALLOWED)

    except Exception as error:
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(error)})


@core_api.post("/{model}", status_code=HTTP_201_CREATED)
async def create_record(request: Request, model):
    try:
        controller.create(model, json.loads(await request.body()))
        return JSONResponse(
            status_code=HTTP_201_CREATED,
            content={})

    except NotImplementedError:
        return JSONResponse(status_code=HTTP_405_METHOD_NOT_ALLOWED)

    except ServiceException as error:
        return JSONResponse(
            status_code=HTTP_409_CONFLICT,
            content={"error": str(error)})

    except Exception as error:
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(error)})


@core_api.put("/{model}/{record_id}", status_code=HTTP_200_OK)
async def update_record(request: Request, model, record_id):
    try:
        controller.update(model, record_id, json.loads(await request.body()))
        return JSONResponse(content={})

    except KeyError:
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={})

    except NotImplementedError:
        return JSONResponse(status_code=HTTP_405_METHOD_NOT_ALLOWED)

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content={"error": str(error)})


@core_api.delete("/{model}/{record_id}", status_code=HTTP_204_NO_CONTENT)
def delete_record(model, record_id):
    try:
        controller.delete(model, record_id)
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    except NotImplementedError:
        return JSONResponse(status_code=HTTP_405_METHOD_NOT_ALLOWED)

    except KeyError:
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={})

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content={"error": str(error)})
