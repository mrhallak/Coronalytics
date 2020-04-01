import requests
import logging

from typing import List, Dict
from src.utils.elastic import Elastic
from src.utils.utils import generate_document


class JhuFetcher:
    @staticmethod
    def fetch_by_country(**kwargs) -> List[Dict]:
        try:
            logging.info("Fetching data by country from JHU")
            url = f"https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query?f=json&where=Confirmed%20%3E%200&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=200&cacheHint=true"

            response = requests.get(url)
            logging.info("Retrieved the data by country from JHU")

            data = response.json()["features"]

            documents = []

            for entry in data:
                body = entry["attributes"]

                documents.append(
                    generate_document(body, kwargs["current_execution_date"])
                )

            return documents

        except Exception as e:
            logging.error(e)
            raise

    @staticmethod
    def load_data(**kwargs):
        ti = kwargs["task_instance"]

        data = ti.xcom_pull(task_ids=kwargs["pull_from"])

        with Elastic() as ecs:
            ecs.index(kwargs["index_name"], data, chunk_size=10000)
