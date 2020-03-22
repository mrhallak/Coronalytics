import datetime
import os

# Airflow
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

# Google Cloud DataProc
from airflow.contrib.operators.dataproc_operator import DataprocClusterCreateOperator, DataprocClusterDeleteOperator, DataProcPySparkOperator

# Other
from data.jhuFetcher import JhuFetcher
from utils.storage import Storage

default_args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(58),
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

# gcp_storage = Storage(project_id=os.environ['GCP_PROJECT_ID'])

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

# create_dataproc_cluster = DataprocClusterCreateOperator(
#     task_id='create_dataproc_cluster',
#     dag=dag,
#     cluster_name=os.environ['GCP_CLUSTER_NAME'],
#     region=os.environ['GCP_CLUSTER_REGION'],
#     project_id=os.environ['GCP_PROJECT_ID'],
#     master_machine_type='n1-standard-1',
#     worker_machine_type='n1-standard-1',
#     num_workers=2,
#     storage_bucket=os.environ['GCP_STORAGE_BUCKET']
# )

fetch_data >> [load_data_in_pg]
load_data_in_pg >> [delete_local_file]


# submit_job = DataProcPySparkOperator(
#     task_id='count_items',
#     dag=dag,
#     main="file://main.py",
#     job_name="count_items",
#     cluster_name=os.environ['GCP_CLUSTER_NAME'],
#     region=os.environ['GCP_CLUSTER_REGION']
# )

# delete_dataproc_cluster = DataprocClusterDeleteOperator(
#     task_id='delete_dataproc_cluster',
#     dag=dag,
#     cluster_name=os.environ['GCP_CLUSTER_NAME'],
#     region=os.environ['GCP_CLUSTER_REGION'],
#     project_id=os.environ['GCP_PROJECT_ID']
# )

# fetch_data.set_upstream(upload_data_to_gcs)
# create_dataproc_cluster.set_upstream(submit_job)

# submit_job.set_upstream(
#     [
#         delete_dataproc_cluster
#     ]
# )