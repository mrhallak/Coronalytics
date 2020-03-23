import datetime
import os

# Airflow
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

# Other
from data.jhuFetcher import JhuFetcher
from utils.storage import Storage

default_args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(60),
    'depends_on_past': False,
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
}

dag = DAG(
    'data_pipeline',
    default_args=default_args,
    description='DAG to extract, transform and load data related to the Corona virus (COVID-19)',
    schedule_interval=datetime.timedelta(days=1),
)

fetch_data = PythonOperator(
    task_id='fetch_data',
    python_callable=JhuFetcher.fetch,
    provide_context=True,
    op_kwargs={'current_execution_date': "{{ ds }}"},
    dag=dag
)

load_data_in_pg = PythonOperator(
    task_id='load_data',
    python_callable=JhuFetcher.load_to_pg,
    op_kwargs={'current_execution_date': "{{ ds }}"},
    dag=dag
)

delete_local_file = BashOperator(
    task_id='delete_temp_file',
    bash_command='rm -rf /tmp/{{ ds }}.csv',
    dag=dag,
)

fetch_data >> [load_data_in_pg]
load_data_in_pg >> [delete_local_file]