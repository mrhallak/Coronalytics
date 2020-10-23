import logging
import os

from elasticsearch import Elasticsearch, helpers
from typing import Iterator


class Elastic:
    def __init__(self, **kwargs):
        """Constructor, creates an
        elasticsearch client and checks if
        we are able to connect to the cluster.

        Args:
            **kwargs: Optional args to connect to your ES cluster
                ELASTICSEARCH_USERNAME: Username
                ELASTICSEARCH_PASSWORD: Password
                ELASTICSEARCH_HOST: Host
                ELASTICSEARCH_PORT: Port
        """
        try:
            username = (
                kwargs["username"] if "username" in kwargs else os.environ["ELASTICSEARCH_USERNAME"]
            )
            password = (
                kwargs["password"] if "password" in kwargs else os.environ["ELASTIC_PASSWORD"]
            )
            host = kwargs["host"] if "host" in kwargs else os.environ["ELASTICSEARCH_HOST"]
            port = kwargs["port"] if "port" in kwargs else os.environ["ELASTICSEARCH_PORT"]

            hosts = [f"http://{username}:{password}@{host}:{port}"]

            self.elastic_client = Elasticsearch(hosts)

            if not self.elastic_client.ping():
                raise ValueError("Connection failed")

        except Exception as e:
            logging.error(e)
            raise

    def __enter__(self) -> object:
        """This function allows us to use
        context management in python. This
        function will be executed when the
        object is created with the "with"
        keyword.

        Returns: Elastic object
        """
        return self

    def __exit__(self, *args):
        """This function is executed when
        we are done using the object created.
        It will make sure to close the open
        connection made to the database.

        Args:
            *args: Args passed to constructor
        """
        logging.info("Closing connection to ElasticSearch")
        self.elastic_client.transport.close()
        logging.info("Closed connection to ElasticSearch")

    def create_index(self, index_name: str, mapping: dict) -> None:
        """This function creates an index on
        the ElasticSearch cluster and ignores any
        errors if the index already exists.

        Args:
            index_name: Name of the index to be created
            mapping: Dict mapping keys to the type of their values
        """
        self.elastic_client.indices.create(index=index_name, body=mapping, ignore=[400])

    def index(self, index_name: str, data: Iterator, chunk_size: int = 100000):
        """This function streams to the cluster in bulk the data
        contained in an iterator.

        Args:
            index_name: Name of the index to store the documents in
            data: Documents iterator
            chunk_size: Size of the chunks to stream (default: {100000})
        """
        failed = 0
        total = 0

        for success, _ in helpers.streaming_bulk(
            self.elastic_client,
            data,
            chunk_size=chunk_size,
            index=index_name,
            max_retries=20,
            request_timeout=120,
        ):
            if not success:
                failed += 1

        total += 1

        return total, failed
