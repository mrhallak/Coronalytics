import pytest

from datetime import datetime
from src.data.jhuFetcher import JhuFetcher

CURRENT_EXECUTION_DATE = datetime.now()


@pytest.fixture()
def data():
    return JhuFetcher.fetch_by_country(current_execution_date=CURRENT_EXECUTION_DATE)


class TestJhuFetcher:
    def test_fetch_by_country_response_type(self, data):
        assert type(data) == list
        assert type(data[0]) == dict

    def test_fetch_by_country_valid_response(self, data):
        assert len(data) > 0