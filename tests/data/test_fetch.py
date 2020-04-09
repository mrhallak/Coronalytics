import pytest

from requests.exceptions import HTTPError
from src.data.fetch import JhuFetcher, JhuApiError
from unittest.mock import patch, MagicMock


class TestJhuFetcher:
    @patch("src.data.fetch.requests")
    def test_fetch_by_country_api_error(self, mock_requests):
        mock_response = MagicMock()
        mock_requests.get.return_value = mock_response
        mock_response.json.return_value = {"error": "Too many requests."}

        with pytest.raises(JhuApiError):
            country_stats = JhuFetcher.fetch_by_country()
            mock_response.raise_for_status.assert_called()

    @patch("src.data.fetch.requests")
    def test_fetch_by_country_json_error(self, mock_requests):
        mock_response = MagicMock()
        mock_requests.get.return_value = mock_response
        mock_response.json.side_effect = ValueError

        with pytest.raises(ValueError):
            country_stats = JhuFetcher.fetch_by_country()

    @patch("src.data.fetch.requests")
    def test_fetch_by_country_request_error(self, mock_requests):
        mock_response = MagicMock()
        mock_requests.get.return_value = mock_response
        mock_response.json.side_effect = HTTPError

        with pytest.raises(HTTPError):
            country_stats = JhuFetcher.fetch_by_country()

    @patch("src.data.fetch.requests")
    def test_fetch_by_country_succeeds(self, mock_requests):
        expected = [
            {
                "attributes": {
                    "OBJECTID": 18,
                    "Country_Region": "US",
                    "Last_Update": 1586364883000,
                    "Lat": 40,
                    "Long_": -100,
                    "Confirmed": 402923,
                    "Deaths": 13007,
                    "Recovered": 22717,
                    "Active": 0,
                }
            },
            {
                "attributes": {
                    "OBJECTID": 161,
                    "Country_Region": "Spain",
                    "Last_Update": 1586364865000,
                    "Lat": 40.463667,
                    "Long_": -3.74922,
                    "Confirmed": 146690,
                    "Deaths": 14673,
                    "Recovered": 48021,
                    "Active": 83996,
                }
            },
        ]

        mock_response = MagicMock()
        mock_requests.get.return_value = mock_response
        mock_response.json.return_value = {"features": expected}

        country_stats = JhuFetcher.fetch_by_country()

        assert country_stats == expected
        mock_response.raise_for_status.assert_called()
