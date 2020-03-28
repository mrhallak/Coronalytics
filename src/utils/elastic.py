import logging
import datetime
from elasticsearch import Elasticsearch, helpers

class Elastic:
    def __init__(self, **kwargs):
        try:
            hosts = [
                f"http://elastic:changeme@elasticsearch:9200"
            ]

            self.elastic_client = Elasticsearch(hosts)

            if not self.elastic_client.ping():
                raise ValueError("Connection failed")

        except Exception as e:
            logging.error(e)

    def __enter__(self) -> object:
        """This function allows us to use
        context management in python. This 
        function will be executed when the
        object is created with the "with"
        keyword.
        
        Returns:
            object -- Elastic object
        """
        return self

    def __exit__(self, *args):
        """This function is executed when
        we are done using the object created.
        It will make sure to close the open
        connection made to the database.
        """
        logging.info("Closing connection to ElasticSearch")
        self.elastic_client.transport.close()
        logging.info("Closed connection to ElasticSearch")


    def index(self, index_name, data, chunk_size=100000):
        failed = 0
        total = 0

        for success, info in helpers.streaming_bulk(self.elastic_client, data, chunk_size=chunk_size, index=index_name, max_retries=20, request_timeout=120):
            if not success:
                failed += 1

        total += 1

        return total, failed