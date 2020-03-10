import datetime
import os

# Airflow
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.dataproc_operator import DataprocClusterCreateOperator, DataprocClusterDeleteOperator

default_args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(1),
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
    # Continue to run DAG once per day
    schedule_interval=datetime.timedelta(days=1),
)

t1 = BashOperator(
    task_id='fetch_data',
    bash_command='date',
    dag=dag
)

t2 = DataprocClusterCreateOperator(
    task_id='create_dataproc_cluster',
    dag=dag,
    cluster_name=os.environ['GCP_CLUSTER_NAME'],
    region=os.environ['GCP_CLUSTER_REGION'],
    project_id=os.environ['GCP_PROJECT_ID'],
    master_machine_type='n1-standard-1',
    worker_machine_type='n1-standard-1',
    num_workers=2
)

t4 = BashOperator(
    task_id='sleep',
    bash_command='sleep 60',
    dag=dag
)

t3 = DataprocClusterDeleteOperator(
    task_id='delete_dataproc_cluster',
    dag=dag,
    cluster_name=os.environ['GCP_CLUSTER_NAME'],
    region=os.environ['GCP_CLUSTER_REGION'],
    project_id=os.environ['GCP_PROJECT_ID']
)

t1 >> t2 >> t4 >> t3