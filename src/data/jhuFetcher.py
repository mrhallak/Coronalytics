import requests
import logging
import json

from typing import List, Dict
from utils.elastic import Elastic

class JhuFetcher:
    @staticmethod
    def fetch_by_country(**kwargs) -> List[Dict]:
        try:
            logging.info("Fetching data by country from JHU")
            url = f"https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query?f=json&where=Confirmed%20%3E%200&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=200&cacheHint=true"

            response = requests.get(url)
            logging.info("Retrieved the data by country from JHU")

            data = response.json()['features']

            documents = []

            for entry in data:
                body = entry['attributes']

                documents.append({
                    "updated": kwargs['current_execution_date'],
                    "confirmed": body['Confirmed'],
                    "deaths": body['Deaths'],
                    "recovered": body['Recovered'],
                    "geoip": {
                        "location": {
                            "lon": body['Long_'],
                            "lat": body['Lat']
                        },
                        "country_name": body['Country_Region'],
                    }
                })

            return documents

        except Exception as e:
            logging.error(e)
    
    @staticmethod
    def load_data(**kwargs):
        ti = kwargs['task_instance']

        data = ti.xcom_pull(task_ids='fetch_data_by_country')

        with Elastic() as ecs:
            ecs.index(kwargs['index_name'], data, chunk_size=10000)