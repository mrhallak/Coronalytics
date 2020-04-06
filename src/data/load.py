from src.utils.elastic import Elastic


class Loader:
    @staticmethod
    def load_data(**kwargs):
        """This function grabs
        data from the XCom and loads it
        into the ES cluster in chunks
        """        
        ti = kwargs["task_instance"]

        data = ti.xcom_pull(task_ids=kwargs["pull_from"])

        with Elastic() as ecs:
            ecs.index(kwargs["index_name"], data, chunk_size=10000)
