import requests
import logging

from typing import List, Dict


class JhuApiError(requests.RequestException):
    def __init__(self, *args, **kwargs):
        """Initialize RequestException with `request` and `response` objects.

        Args:
            *args:
            **kwargs:
        """
        self.details = kwargs.pop("details", None)
        super(JhuApiError, self).__init__(*args, **kwargs)


class JhuFetcher:
    @staticmethod
    def fetch_by_country() -> List[Dict]:
        """This function calls the JHU
        COVID-19 API and gets the daily
        statistics by country.

        Returns:
            List of dictionnaries, each dict contains the stats of a country
        """
        logging.info("Fetching data by country from JHU.")
        url = f"https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query?f=json&where=Confirmed%20%3E%200&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=200&cacheHint=true"

        response = requests.get(url)
        response.raise_for_status()

        json_data = response.json()

        if "error" not in json_data:
            logging.info("Retrieved the data by country from JHU successfully.")
            return json_data["features"]
        else:
            logging.error("Error fetching the data.")
            raise JhuApiError(response=response, details=json_data["error"])
