FROM apache/airflow:2.4.3-python3.7

# Install requirements
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Copy script for health check
COPY ./health_check.py ./health_check.py
