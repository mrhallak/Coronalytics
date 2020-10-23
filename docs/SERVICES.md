# Services
This file contains a description of all of the services used in this project.

## Service list
### ElasticSearch
ElasticSearch is a NoSQL distributed database which we will use to store data.

### Kibana
Kibana is a visualization tool that we will use to visualize the data loaded into ElasticSearch.

### Apache Airflow
Airflow is an orchestration tool that allows us to run a DAG (Direct Acyclic Graph), in other words a set of tasks in a particular order. We will be using Airflow to schedule our DAG, which is the ETL pipeline, daily after Johns Hopkins University updates their data.

### Portainer
Portainer allows you to build and manage your docker containers.

### Postgres
Postgres will allow Airflow to store metadata about our DAGs.

## Service-port mapping
| Service | Port |
| --- | --- |
| Airflow | 8080 |
| Portainer | 9090 |
| ElasticSearch | 9200 |
| Kibana | 5601 |
| Postgres | 5432 |
