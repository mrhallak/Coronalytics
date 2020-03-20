# Services
This file contains a description of all of the services used in this project.

## Service list
### Postgres
Postgres is a SQL database that we will use to store our transformed data.

### Superset
Superset is a visualization tool that we will use to visualize the data loaded into Postgres.
### Jupyter

### Apache Airflow
Airflow is an orchestration tool that allows us to run a DAG (Direct Acyclic Graph), in other words a set of tasks in a particular order. We will be using Airflow to schedule our DAG, which is the ETL pipeline, daily after Johns Hopkins University updates their data.

#### Authenticating with Google Cloud
Please follow this [tutorial][1] in order to authenticate with Google Cloud.

### Portainer
Portainer allows you to build and manage your docker containers.

## Service-port mapping
| Service | Port |
| --- | --- |
| Airflow | 8080 |
| Jupyter | 8888 |
| Portainer | 9090 |
| Postgres | 5432 |
| Superset | 8088 |

[1]: https://cloud.google.com/composer/docs/how-to/managing/connections#creating_new_airflow_connections