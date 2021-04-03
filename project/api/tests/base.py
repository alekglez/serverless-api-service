# -*- coding: utf-8 -*-

from unittest import TestCase
from starlette.testclient import TestClient
from main import create_app


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.app = create_app(app_name='project-test-execution', debug=False)
        self.client = TestClient(self.app)
