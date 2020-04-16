import pytest
from airflow.models import DagBag

DAG_FOLDER = "./src/dags"
DAG_ID = "data_pipeline"


@pytest.fixture(scope="module")
def dagbag():
    return DagBag(dag_folder=DAG_FOLDER, include_examples=False)


@pytest.fixture(scope="module")
def dag(dagbag):
    dag = dagbag.get_dag(dag_id=DAG_ID)

    return dag
