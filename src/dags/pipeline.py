import datetime
import os

# Airflow
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

# Other
from data.jhuFetcher import JhuFetcher

default_args = {
    "owner": "airflow",
    "start_date": airflow.utils.dates.days_ago(1),
    "depends_on_past": False,
    "email": [""],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
}

dag = DAG(
    "data_pipeline",
    default_args=default_args,
    description="DAG to extract, transform and load data related to the Corona virus (COVID-19)",
    schedule_interval=datetime.timedelta(days=1),
)

fetch_data_by_country = PythonOperator(
    task_id="fetch_data_by_country",
    python_callable=JhuFetcher.fetch_by_country,
    provide_context=True,
    op_kwargs={"current_execution_date": "{{ ds }}"},
    dag=dag,
)

load_data_by_country = PythonOperator(
    task_id="load_data_by_country",
    python_callable=JhuFetcher.load_data,
    op_kwargs={"index_name": "by_country"},
    provide_context=True,
    dag=dag,
)

fetch_data_by_country >> [load_data_by_country]