# -*- coding: utf-8 -*-

from project.api.services.dynamo_service import DynamoService
from project.api.services.mock_service import MockService


mapper = {
    "mocks": MockService(),
    "users": DynamoService()
}
