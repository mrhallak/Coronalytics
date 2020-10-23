FROM puckel/docker-airflow

USER root

# Install requirements
ADD ./requirements.txt .
RUN pip install -r requirements.txt

# Copy script for health check
COPY ./health_check.py ./health_check.py
