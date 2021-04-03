# -*- coding: utf-8 -*-

from unittest.mock import patch

from project.api.services.mock_service import mock
from project.api.tests.base import BaseTestCase


class GenericEndpointsTestCases(BaseTestCase):
    def test_get(self):
        response = self.client.get("/api/mocks/")
        assert response.status_code == 200
        assert response.json() == [value for _, value in mock["mocks"].items()]

    def test_get_with_error(self):
        with patch("project.api.controllers.main.Controller.get_all", side_effect=Exception("Error")):
            response = self.client.get("/api/mocks/")
            assert response.status_code == 500

    def test_get_one_record(self):
        response = self.client.get("/api/mocks/000-1")
        assert response.status_code == 200
        assert response.json() == mock["mocks"]["000-1"]

    def test_get_one_record_with_error(self):
        with patch("project.api.controllers.main.Controller.get", side_effect=Exception("Error")):
            response = self.client.get("/api/mocks/000-1")
            assert response.status_code == 500

    def test_get_not_found(self):
        response = self.client.get("/api/mocks/000-5")
        assert response.status_code == 404
        assert response.json() == {}

    def test_post(self):
        payload = {
            "id": "000-3",
            "name": "Some New Service",
            "Description": "Some fancy new service...",
            "value": 5.50
        }

        response = self.client.post("/api/mocks", json=payload)
        assert response.status_code == 201

        response = self.client.post("/api/mocks", json=payload)
        assert response.status_code == 409

        response = self.client.get("/api/mocks/000-3")
        assert response.status_code == 200
        assert response.json() == payload

    def test_post_with_error(self):
        with patch("project.api.controllers.main.Controller.create", side_effect=Exception("Error")):
            response = self.client.post("/api/mocks", json={})
            assert response.status_code == 500

    def test_put(self):
        response = self.client.put("/api/mocks/000-2", json={"name": "New Name"})
        assert response.status_code == 200

        response = self.client.get("/api/mocks/000-2")
        assert response.status_code == 200
        assert response.json()["name"] == "New Name"

    def test_put_not_found(self):
        response = self.client.put("/api/mocks/000-X", json={"name": "New Name"})
        assert response.status_code == 404

    def test_put_with_error(self):
        with patch("project.api.controllers.main.Controller.update", side_effect=Exception("Error")):
            response = self.client.put("/api/mocks/000-2", json={"name": "New Name"})
            assert response.status_code == 500

    def test_delete(self):
        payload = {
            "id": "000-4",
            "name": "Some New Service",
            "Description": "Some fancy new service...",
            "value": 5.50
        }

        response = self.client.post("/api/mocks", json=payload)
        assert response.status_code == 201

        response = self.client.delete("/api/mocks/000-4")
        assert response.status_code == 204

    def test_delete_not_found(self):
        response = self.client.delete("/api/mocks/000-5")
        assert response.status_code == 404

    def test_delete_with_error(self):
        with patch("project.api.controllers.main.Controller.delete", side_effect=Exception("Error")):
            response = self.client.delete("/api/mocks/000-5")
            assert response.status_code == 500
