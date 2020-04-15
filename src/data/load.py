import logging
from src.service.elastic import Elastic


class Loader:
    @staticmethod
    def load_data(chunk_size: int = 10000, **kwargs):
        """This function grabs
        data from the XCom and loads it
        into the ES cluster in chunks

        Args:
            chunk_size: Number of items in a chunk (default: 10000)
            **kwargs:
                task_instance: Task instance from the DAG
                pull_from: ID of the dask to pull the data from the XCOM
                index_name: Name of the index to store the documents in
        """
        ti = kwargs["task_instance"]

        data = ti.xcom_pull(task_ids=kwargs["pull_from"])

        with Elastic() as ecs:
            total, failed = ecs.index(kwargs["index_name"], data, chunk_size=chunk_size)

            log_level = logging.DEBUG if not failed else logging.WARNING

            logging.log(
                log_level, f"Indexing outcome - Total: {total} - Failed {failed}"
            )
