import logging
import os

from typing import Iterator
from psycopg2 import OperationalError, connect

class Postgres:
    def __init__(self, **kwargs):
        """Constructor for the PostgreSQL
        wrapper. If a dictionnary of arguments
        is passed, then the connection to the 
        database is based on the dictionnary else
        it will use environment variables.

        Arguments:
            host {str} -- Ip/Host of the database instance
            database {str} -- Database name
            user {str} -- Username
            password {str} -- Password for authentication
            port {int} -- Port to connect to
        """        
        try:
            host = os.environ['POSTGRES_HOST'] if 'host' not in kwargs else kwargs['host']
            database = os.environ['POSTGRES_DB'] if 'database' not in kwargs else kwargs['database']
            user = os.environ['POSTGRES_USER'] if 'user' not in kwargs else kwargs['user']
            password = os.environ['POSTGRES_PASSWORD'] if 'password' not in kwargs else kwargs['password']
            port = os.environ['POSTGRES_PORT'] if 'port' not in kwargs else kwargs['port']

            logging.info(f"Initiating connection to PostgreSQL ({host}:{port})")

            self.connection = connect(
                database=database,
                host=host,
                port=port,
                user=user,
                password=password
            )

            self.connection.autocommit = False

        except OperationalError as e:
            logging.error(f"Unable to connect to PostgreSQL ({host}:{port})")
            logging.error(e)

    def __enter__(self) -> object:
        """This function allows us to use
        context management in python. This 
        function will be executed when the
        object is created with the "with"
        keyword.
        
        Returns:
            object -- Postgres object
        """        
        return self

    def __exit__(self, *args):
        """This function is executed when
        we are done using the object created.
        It will make sure to close the open
        connection made to the database.
        """        
        logging.info("Closing connection to PostgreSQL")
        self.connection.close()
        logging.info("Closed connection to PostgreSQL")
    
    def execute_query(self, query: str):
        """This function executes a query on PostgreSQL
        
        Arguments:
            query {str} -- Query to be executed
        """        
        try:
            logging.info("Executing query")
            logging.info(f"{query}")

            cursor = self.connection.cursor()
            cursor.execute(query)
            cursor.commit()
            cursor.close()

            logging.info(f"Operation succeeded")
        except Exception as e:
            logging.error(f"Operation failed, rolling back")
            self.connection.rollback()
            logging.error(e)

    def load_data(self, data: Iterator, table_name: str, seperator: str = ',', buffer_size: int = 65536):
        """This function loads data from an
        iterator to PostgreSQL.
        
        Arguments:
            data {Iterator} -- Iterator containing the data
            table_name {str} -- Table to import the data to
        
        Keyword Arguments:
            seperator {str} -- Delimiter that seperates the data (default: {','})
            buffer_size {int} -- Size of the chunks (default: {65536})
        """        
        try:
            logging.info("Importing data to PostgreSQL")
            
            cursor = self.connection.cursor()
            cursor.copy_from(data, table_name, sep=seperator, size=buffer_size)
            cursor.commit()
            cursor.close()

            logging.info("Done importing data to PostgreSQL")
        except Exception as e:
            logging.error("Error importing data to PostgreSQL")
            logging.error(e)