FROM puckel/docker-airflow

USER root


ADD ./services/airflow/airflow.cfg /usr/local/airflow/airflow.cfg
ADD ./requirements.txt .

RUN pip install -r requirements.txt