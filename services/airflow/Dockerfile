FROM puckel/docker-airflow

USER root

ADD ./requirements.txt .
ADD ./gcp-service-account.json .
RUN pip install -r requirements.txt