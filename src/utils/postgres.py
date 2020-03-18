import logging

from typing import Iterator
from psycopg2 import OperationalError, connect

class Postgres:
    def __init__(self, host, password, database="postgres", user="postgres", port=5432):
        try:
            logging.info(f"Initiating connection to PostgreSQL ({host}:{port})")

            self.connection = connect(
                db_name=database,
                host=host,
                port=port,
                user=user,
                password=password
            )

        except OperationalError as e:
            logging.error(e)

    def __enter__(self) -> object:
        return self.connection

    def __exit__(self, *args):
        logging.info("Closing connection to PostgreSQL")
        self.connection.close()
        logging.info("Closed connection to PostgreSQL")

    def load_file(self, data: Iterator, table_name: str, seperator: str =',', buffer_size: int = 65536):
        logging.info("Importing data to PostgreSQL")
        
        cursor = self.connection.cursor()
        cursor.copy_from(data, table_name, sep=seperator, size=buffer_size)
        cursor.close()

        logging.info("Done importing data to PostgreSQL")