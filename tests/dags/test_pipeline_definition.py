import pytest

from airflow.models import DagBag

TASK_IDS = ['create_index', 'fetch_data_by_country', 'transform_data_by_country', 'load_data_by_country']


@pytest.fixture()
def dag():
    dagbag = DagBag(dag_folder="./src/dags", include_examples=False)
    dag = dagbag.get_dag(dag_id="data_pipeline")

    return dag


class TestDAGDefinition:
    """
    This class tests:
        1. Total number of tasks in the DAG
        2. upstream and downstream dependencies of each task
    """
    def test_dag_has_tasks(self, dag):
        """
        This function checks if the DAG
        has the correct number of tasks
        :param dag: Graph to test
        """
        assert len(dag.tasks) == 4

    def test_dag_contain_tasks(self, dag):
        """
        This function checks if the DAG
        has the correct tasks
        :param dag: Graph to test
        """
        dag_tasks = dag.tasks
        dag_task_ids = list(
            map(
                lambda task: task.task_id
                , dag_tasks
            )
        )

        assert dag_task_ids == TASK_IDS

    def test_dependencies_of_create_index(self, dag):
        """
        This function checks if the create_index
        task has the correct upstream and downstream
        dependencies.
        :param dag: Graph to test
        """
        create_index = dag.get_task('create_index')

        upstream_task_ids = list(
            map(
                lambda task: task.task_id,
                create_index.upstream_list
            )
        )

        assert upstream_task_ids == []

        downstream_task_ids = list(
            map(
                lambda task: task.task_id,
                create_index.downstream_list
            )
        )

        assert downstream_task_ids == ['fetch_data_by_country']

    def test_dependencies_of_fetch_data_by_country(self, dag):
        """
        This function checks if the fetch_data_by_country
        task has the correct upstream and downstream
        dependencies.
        :param dag: Graph to test
        """
        fetch_data_by_country = dag.get_task('fetch_data_by_country')

        upstream_task_ids = list(
            map(
                lambda task: task.task_id,
                fetch_data_by_country.upstream_list
            )
        )

        assert upstream_task_ids == ['create_index']

        downstream_task_ids = list(
            map(
                lambda task: task.task_id,
                fetch_data_by_country.downstream_list
            )
        )

        assert downstream_task_ids == ['transform_data_by_country']

    def test_dependencies_of_transform_data_by_country(self, dag):
        """
        This function checks if the transform_data_by_country
        task has the correct upstream and downstream
        dependencies.
        :param dag: Graph to test
        """
        fetch_data_by_country = dag.get_task('transform_data_by_country')

        upstream_task_ids = list(
            map(
                lambda task: task.task_id,
                fetch_data_by_country.upstream_list
            )
        )

        assert upstream_task_ids == ['fetch_data_by_country']

        downstream_task_ids = list(
            map(
                lambda task: task.task_id,
                fetch_data_by_country.downstream_list
            )
        )

        assert downstream_task_ids == ['load_data_by_country']

    def test_dependencies_of_load_data_by_country(self, dag):
        """
        This function checks if the load_data_by_country
        task has the correct upstream and downstream
        dependencies.
        :param dag: Graph to test
        """
        fetch_data_by_country = dag.get_task('load_data_by_country')

        upstream_task_ids = list(
            map(
                lambda task: task.task_id,
                fetch_data_by_country.upstream_list
            )
        )

        assert upstream_task_ids == ['transform_data_by_country']

        downstream_task_ids = list(
            map(
                lambda task: task.task_id,
                fetch_data_by_country.downstream_list
            )
        )

        assert downstream_task_ids == []