# -*- coding: utf-8 -*-

from typing import Any, Dict
from project.api.services.base import Service
from project.api.configs.service_mapper import mapper


class Controller:
    def __init__(self, services: str):
        """
        Initialize the services...
        :param services: String that contains the service names (coma separated)
        """

        services = services.split(",")
        self.services = [Service.create_class(service)() for service in services]
        self.mapper = mapper

    def __get_service(self, model: str):
        """
        Try to find a service for the given model...

        :param model: Model to use
        :return: The Service associated to the model.
        """

        try:
            return self.mapper[model]

        except KeyError:
            raise ControllerException("No service associated to the requested resource!")

    def get_all(self, model: str, filters, fields, offset, limit):
        return self.__get_service(model).get_records(
            model, filters, fields, offset, limit)

    def get(self, model: str, record_id: Any):
        return self.__get_service(model).get_record(model, record_id)

    def create(self, model: str, values: Dict):
        self.__get_service(model).create_record(model, values["id"], values)

    def update(self, model: str, record_id: Any, values: Dict):
        self.__get_service(model).update_record(model, record_id, values)

    def delete(self, model: str, record_id: Any):
        self.__get_service(model).delete_record(model, record_id)


class ControllerException(Exception):
    """ Custom class for controller exceptions """
