# -*- coding: utf-8 -*-

from typing import Any, Dict, Iterable, List, Tuple
from project.api.services.base import Service, ServiceException


mock = {
    "mocks": {
        "000-1": {
            "id": "000-1",
            "name": "Service",
            "Description": "Some fancy description...",
            "value": 50.0
        },
        "000-2": {
            "id": "000-2",
            "name": "Gas Station",
            "Description": "Some fancy gas station...",
            "value": 1.5
        }
    }
}


class MockService(Service):
    def get_records(self, model: str, filters: List[Tuple], fields: List[str],
                    offset: int = 0, limit: int = 20) -> Iterable:

        return [value for _, value in mock.get(model, {}).items()]

    def get_record(self, model: str, record_id: Any) -> Any:
        return mock.get(model, {})[record_id]

    def create_record(self, model: str, record_id: Any, record_values: Dict):
        if record_id in mock[model]:
            raise ServiceException(f"Record with id {record_id}, already exist!")

        mock[model][record_values["id"]] = record_values

    def update_record(self, model: str, record_id: Any, values: Dict):
        for key, value in values.items():
            mock[model][record_id][key] = value

    def delete_record(self, model: str, record_id: Any):
        del mock[model][record_id]
