# -*- coding: utf-8 -*-

from abc import abstractmethod
from typing import Any, Dict, Iterable, List, Tuple


class Service:
    """
    Abstract Service you need to implement to
    interact with your data storage of preference.
    """

    subclasses = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses[cls.__name__] = cls

    @classmethod
    def create_class(cls, subclass_name: str = None):
        if not subclass_name:
            raise NotImplementedError

        return cls.subclasses.get(subclass_name)

    @abstractmethod
    def get_records(self, model: str, filters: List[Tuple], fields: List[str],
                    offset: int = 0, limit: int = 20) -> Iterable:

        """
        Return records using pagination...

        :param model: Model or object family.
        :param filters: Filters to apply to limit the records to retrieve.
        :param fields: Fields you want to retrieve. If None, return all the object fields.
        :param offset: Start index to retrieve
        :param limit: End index to retrieve.
        :return:
        """

    @abstractmethod
    def get_record(self, model: str, record_id: Any) -> Any:
        """
        Return if exist the record with the specified id...

        :param model: Model or object family.
        :param record_id: Record id.
        :return: The record or None
        """

    @abstractmethod
    def create_record(self, model: str, record_id: Any, record_values: Dict):
        """
        Create a record using the values...

        :param model: Model or object family.
        :param record_id: Record id.
        :param record_values: Dictionary of values.
        :return:
        """

    @abstractmethod
    def update_record(self, model: str, record_id: Any, record_values: Dict):
        """
        Update the record using the values...

        :param model: Model or object family.
        :param record_id: Record id.
        :param record_values: Dictionary of values.
        :return:
        """

    @abstractmethod
    def delete_record(self, model: str, record_id: Any):
        """
        Delete the record...

        :param model: Model or object family.
        :param record_id: Record id.
        :return:
        """


class ServiceException(Exception):
    """ Custom class for service exceptions """
