import requests
import logging

from datetime import datetime
from utils.postgres import Postgres
from utils.utils import file_to_iterable

class JhuFetcher:
    @staticmethod
    def fetch(current_execution_date: str, chunk_size=8192, **context: dict) -> None:
        try:
            execution_date_reformat = datetime.strptime(current_execution_date, '%Y-%m-%d').strftime('%m-%d-%Y')
            logging.info(f"Fetching data from Johns Hopkins University - Daily Reports ({current_execution_date})")

            url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{execution_date_reformat}.csv'
            
            write_path = f"/tmp/{current_execution_date}.csv"

            with requests.get(url, stream=True) as r:
                r.raise_for_status()

                with open(write_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=chunk_size): 
                        if chunk:
                            f.write(chunk)

        except Exception as e:
            logging.error(e)

    @staticmethod
    def load_to_pg(current_execution_date: str):
        fields = ("province","country","last_update","confirmed","deaths","recovered","latitude","longitude")
        file_path = f"/tmp/{current_execution_date}.csv"

        data = file_to_iterable(file_path, fields)

        with Postgres() as pg:
            pg.load_file(data, 'daily_reports')