import requests
import logging
import json

from typing import List, Dict
from datetime import datetime


class JhuFetcher:
    @staticmethod
    def fetch_by_country(**kwargs) -> List[Dict]:
        try:
            url = f"https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query?f=json&where=Confirmed%20%3E%200&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=200&cacheHint=true"

            response = requests.get(url)
            data = response.json()['features']

            documents = []

            for entry in data:
                body = entry['attributes']

                documents.append({
                    "fetch_update": datetime.now(),
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

    # @staticmethod
    # def fetch_by_province() -> List[Dict]:
    #     try:
    #         url = f"https://services9.arcgis.com/N9p5hsImWXAccRNI/arcgis/rest/services/Nc2JKvYFoAEOFCG5JSI6/FeatureServer/3/query?f=json&where=Confirmed%3C%3E0&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=75&cacheHint=true"

    #         response = requests.get(url)
    #         data = response.json()

    #         return data['fields']

    #     except Exception as e:
    #         logging.error(e)
