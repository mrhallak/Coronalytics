import requests
import logging
from datetime import datetime

class JhuFetcher:
    @staticmethod
    def fetch(chunk_size=8192):
        try:
            # current_date = datetime.today().strftime('%m-%d-%Y')
            current_date = '03-14-2020'
            logging.info(f"Fetching data from Johns Hopkins University - Daily Reports ({current_date})")

            url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{current_date}.csv'
            
            local_filename = f"{current_date}.csv"

            with requests.get(url, stream=True) as r:
                r.raise_for_status()

                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=chunk_size): 
                        if chunk:
                            f.write(chunk)
            
            return local_filename
        
        except Exception as e:
            logging.error(e)

JhuFetcher.fetch()