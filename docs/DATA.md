# Data

## Data Source
The data is fetched from the JHU's COVID-19 [dashboard](https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6) API.

## Data persistence
The data is persisted in an index called by_country on ElasticSearch. Each country is a document inside that index.

## Visualization
In order to visualize the data with Kibana, you need to setup your index patterns in the settings page.