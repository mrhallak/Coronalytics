# import pytest

# import airflow
# from airflow import DAG
# from datetime import datetime


# @pytest.fixture
# def create_dag():
#     default_args = {
#         'owner': 'airflow',
#         'start_date': airflow.utils.dates.days_ago(1),
#         'depends_on_past': False,
#         'retries': 1,
#         'retry_delay': datetime.timedelta(minutes=5),
#     }

#     return DAG(
#         'data_pipeline',
#         default_args=default_args,
#         description='DAG to extract, transform and load data related to the Corona virus (COVID-19)',
#         schedule_interval=datetime.timedelta(days=1),
#     )