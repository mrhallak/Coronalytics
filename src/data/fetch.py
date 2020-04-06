import requests
import logging


from typing import List, Dict

class JhuFetcher:
    @staticmethod
    def fetch_by_country() -> List[Dict]:
        """This function calls the JHU
        COVID-19 API and gets the daily
        statistics by country.
        
        Returns:
            List[Dict] -- Each dict contains the stats of a country
        """        
        try:
            logging.info("Fetching data by country from JHU")
            url = f"https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query?f=json&where=Confirmed%20%3E%200&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=200&cacheHint=true"

            response = requests.get(url)

            if response.ok:
                logging.info("Retrieved the data by country from JHU successfully")
                return response
            else:
                return None

        except Exception as e:
            logging.error("Error fetching the data.")
            logging.error(e)
            raise