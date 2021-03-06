import datetime

# Airflow
import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Other
from src.data.fetch import JhuFetcher
from src.data.load import Loader
from src.data.transform import Transformer
from src.service.elastic import Elastic

mapping = {"mappings": {"properties": {"location": {"type": "geo_point"}}}}

index_name = "by_country"

default_args = {
    "owner": "airflow",
    "start_date": airflow.utils.dates.days_ago(1),
    "depends_on_past": False,
    "email": [""],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=15),
}

dag = DAG(
    dag_id="data_pipeline",
    default_args=default_args,
    description="DAG to extract, transform and load data related to the Corona virus (COVID-19)",
    schedule_interval=datetime.timedelta(hours=12),
)

create_index = PythonOperator(
    task_id="create_index",
    python_callable=Elastic().create_index,
    op_kwargs={"index_name": index_name, "mapping": mapping},
    dag=dag,
)

fetch_data_by_country = PythonOperator(
    task_id="fetch_data_by_country", python_callable=JhuFetcher.fetch_by_country, dag=dag,
)

transform_data_by_country = PythonOperator(
    task_id="transform_data_by_country",
    python_callable=Transformer().transform_by_country,
    op_kwargs={
        "index_name": index_name,
        "pull_from": "fetch_data_by_country",
        "current_execution_date": "{{ ts }}",
    },
    provide_context=True,
    dag=dag,
)

load_data_by_country = PythonOperator(
    task_id="load_data_by_country",
    python_callable=Loader.load_data,
    op_kwargs={"index_name": index_name, "pull_from": "transform_data_by_country"},
    provide_context=True,
    dag=dag,
)

create_index >> fetch_data_by_country >> transform_data_by_country >> load_data_by_country
