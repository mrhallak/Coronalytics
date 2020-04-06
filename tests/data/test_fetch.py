import pytest
import requests

from datetime import datetime
from src.data.fetch import JhuFetcher


@pytest.fixture()
def response():
    return JhuFetcher.fetch_by_country()


class TestJhuFetcher:
    def test_fetch_by_country_fails(self, response):
        assert response.status_code != 200

    def test_fetch_by_country_succeeds(self, response):
        assert response.status_code == 200

    def test_fetch_by_country_response_type(self, response):
        data = response.json()["features"]

        assert type(data) == list
        assert type(data[0]) == dict

    def test_fetch_by_country_valid_response(self, response):
        data = response.json()

        assert "features" in data

        assert len(data) > 0
        assert response.json()
