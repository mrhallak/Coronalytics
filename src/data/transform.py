import logging

from typing import List, Dict
from src.data.fetch import JhuFetcher


class Transformer:
    def transform_by_country(self, **kwargs) -> List[Dict]:
        ti = kwargs["task_instance"]

        data = ti.xcom_pull(task_ids=kwargs["pull_from"])

        documents = map(
            lambda e: self.generate_document(
                e["attributes"], kwargs["current_execution_date"]
            ),
            data["features"],
        )

        return documents

    def generate_document(self, body: dict, current_execution_date: str) -> dict:
        """This function helps by convering
        the data scraped from JHU to a
        document that we will store in 
        ElasticSearch.
        
        Arguments:
            body {dict} -- JSON object received
            current_execution_date {str} -- DAG's execution date
        
        Raises:
            TypeError: The passed object is not of type dict

        Returns:
            dict -- Transformed object
        """
        if isinstance(body, dict):
            doc = {
                "updated": current_execution_date,
                "confirmed": body["Confirmed"],
                "deaths": body["Deaths"],
                "recovered": body["Recovered"],
                "location": {"lon": body["Long_"], "lat": body["Lat"]},
                "country_name": body["Country_Region"],
            }

            return doc
        else:
            raise TypeError("Please pass a dictionary")
