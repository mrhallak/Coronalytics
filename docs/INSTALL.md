# Installation
## Requirements
You must have [Docker](http://www.docker.com) installed. Please click on [this tutorial](https://docs.docker.com/install/) if you don't.

## How to run
1. Clone the repository using `git clone https://github.com/mrhallak/Coronalytics.git`
2. Go to the config folder and edit the .env files, add in the credentials you would like to have.
3. Open up a terminal in the root directory.
4. Build the containers using `docker-compose -f docker-compose.local.yml build`
5. Initialize the metadata database `docker-compose -f .\docker-compose.local.yml run webserver db init`
6. Create an admin user `docker-compose -f .\docker-compose.local.yml run webserver airflow users create --username admin --firstname admin --lastname admin --role Admin --email admin@admin.com --password admin`
7. Start the containers using `docker-compose -f docker-compose.local.yml up`
8. Go to [Airflow's home](http://localhost:8080) and turn the DAG on.
9. Go to [Kibana](http://localhost:5601) and create your own dashboard.

Note: docker-compose is using to create and build the services mentioned in [this document](SERVICES.md).
