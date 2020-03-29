# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
## [2.0.0] - 2020-04-01
### Added
- ElasticSearch as a NoSQL database
- Kibana for visualization
### Changed
- Fetching data from the JHU API instead of CSVs from the Github repository
### Removed
- Grafana
- Postgres

## [Released]
## [[1.0.0]](https://github.com/mrhallak/Coronalytics/releases/tag/v1.0.0) - 2020-03-24
### Added
- Docker-compose setup
- Pull data from the [JHU CSSE COVID-19 repository](https://github.com/CSSEGISandData/COVID-19)
- Load data in PostgreSQL
- Visualize using Grafana