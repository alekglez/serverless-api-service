# -*- coding: utf-8 -*-

from project.api.tests.base import BaseTestCase


class HealthTestCases(BaseTestCase):
    def test_ping(self):
        response = self.client.get("/api/ping")
        assert response.status_code == 200
