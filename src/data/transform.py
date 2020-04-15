from typing import Iterator, Dict
from datetime import datetime


class Transformer:
    def transform_by_country(self, **kwargs) -> Iterator[Dict]:
        """Calls on the generate_document function
        to trasnform the dicts in the Iterable

        Args:
            **kwargs: should contain the task instance from the Airflow DAG, current_execution_date and the task id to pull the iterator from the XCOM

        Returns:
            Iterator containg dicts (each dict is a document)
        """
        ti = kwargs["task_instance"]

        data = ti.xcom_pull(task_ids=kwargs["pull_from"])

        documents = list(
            map(
                lambda e: self.generate_document(
                    e["attributes"], kwargs["current_execution_date"]
                ),
                data,
            )
        )

        return documents

    def generate_document(self, body: dict, current_execution_date: datetime) -> dict:
        """This function helps by convering
        the data scraped from JHU to a
        document that we will store in
        ElasticSearch.

        Args:
            body: JSON object received
            current_execution_date: current_execution_date: DAG's execution date

        Returns:
            Transformed dict
        """
        if isinstance(body, dict):
            doc = {
                "updated": current_execution_date,
                "confirmed": body["Confirmed"],
                "deaths": body["Deaths"],
                "recovered": body["Recovered"],
                "country_name": body["Country_Region"],
            }

            if body["Long_"] or body["Lat"]:
                doc["location"] = {"lon": body["Long_"], "lat": body["Lat"]}

            return doc
        else:
            raise TypeError("Please pass a dictionary")
