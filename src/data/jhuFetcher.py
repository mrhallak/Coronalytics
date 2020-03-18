import requests
import logging

from datetime import datetime

class JhuFetcher:
    @staticmethod
    def fetch(current_execution_date: str, chunk_size=8192, **context: dict):
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

            return current_execution_date
        
        except Exception as e:
            logging.error(e)